"""Testes da interface antes da integracao com o modelo."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def test_app_starts_with_welcome_message() -> None:
    app = AppTest.from_file(APP_PATH).run()

    assert not app.exception
    assert app.title[0].value == "English Conversation Coach"
    assert "What would you like to talk about?" in (
        app.chat_message[0].markdown[0].value
    )


def test_app_records_answer_and_mock_response() -> None:
    app = AppTest.from_file(APP_PATH).run()

    app.chat_input[0].set_value("My day was very productive.").run()

    assert len(app.chat_message) == 3
    assert app.chat_message[1].markdown[0].value == "My day was very productive."
    assert "Okay, let's talk about that!" in app.chat_message[2].markdown[0].value
