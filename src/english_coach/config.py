"""Leitura e validacao das configuracoes da aplicacao."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ModelSettings:
    repository: str
    quantization: str
    context_size: int


@dataclass(frozen=True)
class GenerationSettings:
    temperature: float
    top_p: float
    max_tokens: int


@dataclass(frozen=True)
class ApplicationSettings:
    name: str
    log_level: str


class ConfigError(ValueError):
    """Indica que o arquivo de configuracao possui um valor invalido."""


@dataclass(frozen=True)
class Settings:
    model: ModelSettings
    generation: GenerationSettings
    application: ApplicationSettings

def _get_section(data: dict[str, Any], name: str) -> dict[str, Any]:
    section = data.get(name)
    if not isinstance(section, dict):
        raise ConfigError(f"Secao obrigatoria ausente ou invalida: {name}")
    return section


def load_settings(path: str | Path) -> Settings:
    """Carrega o YAML e converte seus valores em configuracoes tipadas."""
    config_path = Path(path)

    try:
        raw_data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ConfigError(f"Arquivo de configuracao nao encontrado: {config_path}") from error
    except yaml.YAMLError as error:
        raise ConfigError("O arquivo de configuracao possui YAML invalido") from error

    if not isinstance(raw_data, dict):
        raise ConfigError("A raiz da configuracao deve ser um objeto YAML")

    model = _get_section(raw_data, "model")
    generation = _get_section(raw_data, "generation")
    application = _get_section(raw_data, "application")

    try:
        settings = Settings(
            model=ModelSettings(
                repository=str(model["repository"]),
                quantization=str(model["quantization"]),
                context_size=int(model["context_size"]),
            ),
            generation=GenerationSettings(
                temperature=float(generation["temperature"]),
                top_p=float(generation["top_p"]),
                max_tokens=int(generation["max_tokens"]),
            ),
            application=ApplicationSettings(
                name=str(application["name"]),
                log_level=str(application["log_level"]),
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigError(f"Campo de configuracao ausente ou invalido: {error}") from error

    if settings.model.context_size <= 0:
        raise ConfigError("model.context_size deve ser maior que zero")
    if not 0 <= settings.generation.temperature <= 2:
        raise ConfigError("generation.temperature deve estar entre 0 e 2")
    if not 0 < settings.generation.top_p <= 1:
        raise ConfigError("generation.top_p deve estar entre 0 e 1")
    if settings.generation.max_tokens <= 0:
        raise ConfigError("generation.max_tokens deve ser maior que zero")

    return settings
