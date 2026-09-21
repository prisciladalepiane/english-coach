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


