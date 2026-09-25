"""Testes da leitura e validacao das configuracoes."""

from pathlib import Path

import pytest

from english_coach.config import ConfigError, load_settings


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_load_project_settings() -> None:
    settings = load_settings(PROJECT_ROOT / "config" / "settings.yaml")

    assert settings.model.repository
    assert settings.model.filename
    assert settings.model.quantization
    assert settings.model.revision
    assert settings.model.context_size > 0
    assert 0 <= settings.generation.temperature <= 2
    assert 0 < settings.generation.top_p <= 1
    assert settings.generation.max_tokens > 0
    assert settings.application.name


def test_load_settings_reads_each_field(tmp_path: Path) -> None:
    config_file = tmp_path / "custom-settings.yaml"
    config_file.write_text(
        """
model:
  repository: Example/Other-GGUF
  filename: other-Q5_K_M.gguf
  quantization: Q5_K_M
  revision: example-commit
  context_size: 2048
generation:
  temperature: 0.3
  top_p: 0.9
  max_tokens: 128
application:
  name: Another Coach
  log_level: DEBUG
""",
        encoding="utf-8",
    )

    settings = load_settings(config_file)

    assert settings.model.repository == "Example/Other-GGUF"
    assert settings.model.filename == "other-Q5_K_M.gguf"
    assert settings.model.quantization == "Q5_K_M"
    assert settings.model.revision == "example-commit"
    assert settings.model.context_size == 2048
    assert settings.generation.temperature == 0.3
    assert settings.generation.top_p == 0.9
    assert settings.generation.max_tokens == 128
    assert settings.application.name == "Another Coach"
    assert settings.application.log_level == "DEBUG"


def test_rejects_invalid_temperature(tmp_path: Path) -> None:
    config_file = tmp_path / "invalid-settings.yaml"
    config_file.write_text(
        """
model:
  repository: Qwen/Qwen3-4B-GGUF
  filename: Qwen3-4B-Q4_K_M.gguf
  quantization: Q4_K_M
  revision: bc64014
  context_size: 4096
generation:
  temperature: 3
  top_p: 0.8
  max_tokens: 512
application:
  name: English Conversation Coach
  log_level: INFO
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="temperature"):
        load_settings(config_file)
