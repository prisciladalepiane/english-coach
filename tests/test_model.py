"""Testes da localizacao e do download controlado do GGUF."""

from pathlib import Path

import pytest

from english_coach.config import GenerationSettings, ModelSettings
from english_coach.model import (
    ModelFileError,
    download_model_file,
    generate_response,
    get_local_model_path,
    is_model_available,
    load_model,
)


MODEL_SETTINGS = ModelSettings(
    repository="Qwen/Qwen3-4B-GGUF",
    filename="Qwen3-4B-Q4_K_M.gguf",
    quantization="Q4_K_M",
    revision="bc64014",
    context_size=4096,
)

GENERATION_SETTINGS = GenerationSettings(
    temperature=0.7,
    top_p=0.8,
    max_tokens=120,
)


def test_model_is_unavailable_before_download(tmp_path: Path) -> None:
    expected_path = tmp_path / MODEL_SETTINGS.filename

    assert get_local_model_path(MODEL_SETTINGS, tmp_path) == expected_path
    assert not is_model_available(MODEL_SETTINGS, tmp_path)


def test_download_uses_pinned_model_revision(tmp_path: Path) -> None:
    received_arguments: dict[str, object] = {}

    def fake_downloader(**kwargs: object) -> str:
        received_arguments.update(kwargs)
        downloaded_file = tmp_path / MODEL_SETTINGS.filename
        downloaded_file.write_bytes(b"fake GGUF")
        return str(downloaded_file)

    model_path = download_model_file(
        MODEL_SETTINGS,
        tmp_path,
        downloader=fake_downloader,
    )

    assert model_path == tmp_path / MODEL_SETTINGS.filename
    assert received_arguments == {
        "repo_id": "Qwen/Qwen3-4B-GGUF",
        "filename": "Qwen3-4B-Q4_K_M.gguf",
        "revision": "bc64014",
        "local_dir": str(tmp_path),
    }
    assert is_model_available(MODEL_SETTINGS, tmp_path)


def test_existing_model_is_not_downloaded_again(tmp_path: Path) -> None:
    model_path = tmp_path / MODEL_SETTINGS.filename
    model_path.write_bytes(b"existing GGUF")

    def unexpected_downloader(**kwargs: object) -> str:
        raise AssertionError(f"Downloader should not be called: {kwargs}")

    result = download_model_file(
        MODEL_SETTINGS,
        tmp_path,
        downloader=unexpected_downloader,
    )

    assert result == model_path


def test_load_model_uses_configured_path_and_context(
    tmp_path: Path,
    monkeypatch,
) -> None:
    model_path = tmp_path / MODEL_SETTINGS.filename
    model_path.write_bytes(b"fake GGUF")
    received_arguments: dict[str, object] = {}
    fake_model = object()

    def fake_llama(**kwargs: object) -> object:
        received_arguments.update(kwargs)
        return fake_model

    monkeypatch.setattr("english_coach.model.Llama", fake_llama)

    result = load_model(MODEL_SETTINGS, tmp_path)

    assert result is fake_model
    assert received_arguments == {
        "model_path": str(model_path),
        "n_ctx": 4096,
        "verbose": False,
    }


def test_load_model_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ModelFileError, match="Modelo nao encontrado"):
        load_model(MODEL_SETTINGS, tmp_path)


def test_generate_response_uses_generation_settings() -> None:
    received_arguments: dict[str, object] = {}

    class FakeModel:
        def create_chat_completion(self, **kwargs: object) -> dict[str, object]:
            received_arguments.update(kwargs)
            return {
                "choices": [
                    {"message": {"content": "  What do you do at work?  "}}
                ]
            }

    messages = [{"role": "user", "content": "I work with data."}]
    response = generate_response(FakeModel(), messages, GENERATION_SETTINGS)

    assert response == "What do you do at work?"
    assert received_arguments == {
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.8,
        "max_tokens": 120,
    }
