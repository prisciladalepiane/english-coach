"""Localizacao e download controlado do arquivo GGUF."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

from llama_cpp import Llama

from english_coach.config import GenerationSettings, ModelSettings


class ModelFileError(RuntimeError):
    """Indica uma falha ao localizar ou baixar o arquivo do modelo."""


class ModelInferenceError(RuntimeError):
    """Indica uma falha ao carregar o modelo ou gerar uma resposta."""


DownloadFunction = Callable[..., str]


def get_local_model_path(
    settings: ModelSettings,
    models_dir: str | Path,
) -> Path:
    """Retorna o caminho esperado para o GGUF local."""
    return Path(models_dir) / settings.filename


def is_model_available(settings: ModelSettings, models_dir: str | Path) -> bool:
    """Informa se o arquivo GGUF configurado ja existe localmente."""
    return get_local_model_path(settings, models_dir).is_file()


def _hugging_face_download(**kwargs: Any) -> str:
    """Importa o cliente apenas quando um download for solicitado."""
    try:
        from huggingface_hub import hf_hub_download
    except ImportError as error:
        raise ModelFileError(
            "huggingface-hub nao esta instalado no ambiente virtual"
        ) from error

    return hf_hub_download(**kwargs)


def download_model_file(
    settings: ModelSettings,
    models_dir: str | Path,
    downloader: DownloadFunction | None = None,
) -> Path:
    """Baixa a revisao configurada do GGUF e retorna seu caminho local."""
    local_path = get_local_model_path(settings, models_dir)
    if local_path.is_file():
        return local_path

    destination = Path(models_dir)
    destination.mkdir(parents=True, exist_ok=True)
    download = downloader or _hugging_face_download

    try:
        downloaded_path = Path(
            download(
                repo_id=settings.repository,
                filename=settings.filename,
                revision=settings.revision,
                local_dir=str(destination),
            )
        )
    except ModelFileError:
        raise
    except Exception as error:
        raise ModelFileError(f"Nao foi possivel baixar o modelo: {error}") from error

    if not downloaded_path.is_file():
        raise ModelFileError(
            f"O download terminou, mas o arquivo nao foi encontrado: {downloaded_path}"
        )

    return downloaded_path


def load_model(settings: ModelSettings, models_dir: str | Path) -> Llama:
    """Carrega o modelo GGUF para a memoria."""
    model_path = get_local_model_path(settings, models_dir)

    if not model_path.is_file():
        raise ModelFileError(f"Modelo nao encontrado: {model_path}")

    try:
        return Llama(
            model_path=str(model_path),
            n_ctx=settings.context_size,
            verbose=False,
        )
    except Exception as error:
        raise ModelInferenceError(
            f"Nao foi possivel carregar o modelo: {error}"
        ) from error


def generate_response(
    model: Llama,
    messages: list[dict[str, str]],
    settings: GenerationSettings,
) -> str:
    """Envia as mensagens ao modelo e retorna somente o texto da resposta."""
    try:
        result = model.create_chat_completion(
            messages=messages,
            temperature=settings.temperature,
            top_p=settings.top_p,
            max_tokens=settings.max_tokens,
        )
        content = result["choices"][0]["message"]["content"]
    except Exception as error:
        raise ModelInferenceError(
            f"Nao foi possivel gerar uma resposta: {error}"
        ) from error

    if not isinstance(content, str) or not content.strip():
        raise ModelInferenceError("O modelo retornou uma resposta vazia")

    return content.strip()
