"""Configuracao centralizada dos logs da aplicacao."""

import logging


LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def configure_logging(level: str) -> logging.Logger:
    """Configura uma unica saida de logs para o terminal."""
    level_name = level.upper()
    if level_name not in LOG_LEVELS:
        raise ValueError(f"Nivel de log invalido: {level}")

    logger = logging.getLogger("english_coach")
    logger.setLevel(LOG_LEVELS[level_name])
    logger.propagate = False

    if not any(
        handler.get_name() == "english_coach_console" for handler in logger.handlers
    ):
        handler = logging.StreamHandler()
        handler.set_name("english_coach_console")
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
        )
        logger.addHandler(handler)

    return logger
