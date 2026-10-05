"""Testes da configuracao de logs sem carregar o modelo."""

import logging

import pytest

from english_coach.logging_config import configure_logging


@pytest.fixture
def isolated_logger(monkeypatch):
    logger = logging.getLogger("english_coach")
    previous_level = logger.level
    monkeypatch.setattr(logger, "handlers", [])
    monkeypatch.setattr(logger, "propagate", True)
    yield logger
    logger.setLevel(previous_level)


def test_configure_logging_uses_level_and_writes_to_terminal(
    isolated_logger, capsys
) -> None:
    logger = configure_logging("INFO")

    logger.debug("Mensagem oculta")
    logger.info("Modelo carregado")

    output = capsys.readouterr().err
    assert logger.level == logging.INFO
    assert "INFO [english_coach] Modelo carregado" in output
    assert "Mensagem oculta" not in output
    assert not logger.propagate


def test_configure_logging_does_not_duplicate_handlers(isolated_logger) -> None:
    logger = configure_logging("INFO")
    configure_logging("DEBUG")

    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 1


def test_configure_logging_rejects_invalid_level(isolated_logger) -> None:
    with pytest.raises(ValueError, match="Nivel de log invalido"):
        configure_logging("VERBOSE")
