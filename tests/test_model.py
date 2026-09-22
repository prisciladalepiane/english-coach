"""Testes da localizacao e do download controlado do GGUF."""

from pathlib import Path

from english_coach.config import ModelSettings
from english_coach.model import (
    download_model_file,
    get_local_model_path,
    is_model_available,
)


MODEL_SETTINGS = ModelSettings(
    repository="Qwen/Qwen3-4B-GGUF",
    filename="Qwen3-4B-Q4_K_M.gguf",
    quantization="Q4_K_M",
    revision="bc64014",
    context_size=4096,
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
