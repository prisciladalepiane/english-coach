"""Teste minimo para confirmar que o pacote pode ser importado."""

from english_coach import __version__


def test_package_version() -> None:
    assert __version__ == "0.1.0"
