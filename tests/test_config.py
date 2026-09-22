"""Testes da leitura e validacao das configuracoes."""

from pathlib import Path

import pytest

from english_coach.config import ConfigError, load_settings


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_load_project_settings() -> None:
    settings = load_settings(PROJECT_ROOT / "config" / "settings.yaml")

    assert settings.model.repository == "Qwen/Qwen3-4B-GGUF"
    assert settings.model.filename == "Qwen3-4B-Q4_K_M.gguf"
    assert settings.model.quantization == "Q4_K_M"
    assert settings.model.revision == "bc64014"
    assert settings.model.context_size == 4096
    assert settings.generation.temperature == 0.7


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
