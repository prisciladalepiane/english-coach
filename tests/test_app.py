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


def test_app_uses_model_and_keeps_conversation(monkeypatch) -> None:
    calls: list[list[dict[str, str]]] = []
    model = object()

    def fake_generate_response(
        received_model: object,
        messages: list[dict[str, str]],
        settings: object,
    ) -> str:
        assert received_model is model
        calls.append(messages)
        return "What do you enjoy about your work?"

    monkeypatch.setattr("english_coach.model.is_model_available", lambda *_: True)
    monkeypatch.setattr("english_coach.model.load_model", lambda *_: model)
    monkeypatch.setattr("english_coach.chat.generate_response", fake_generate_response)

    app = AppTest.from_file(APP_PATH).run()

    app.chat_input[0].set_value("My day was very productive.").run()

    assert len(app.chat_message) == 3
    assert app.chat_message[1].markdown[0].value == "My day was very productive."
    assert app.chat_message[2].markdown[0].value == "What do you enjoy about your work?"
    assert calls[0][-1] == {"role": "user", "content": "My day was very productive."}
    assert calls[0][0]["role"] == "system"

    app.chat_input[0].set_value("I enjoy finding patterns.").run()

    assert len(app.chat_message) == 5
    assert calls[1][-3:] == [
        {"role": "user", "content": "My day was very productive."},
        {"role": "assistant", "content": "What do you enjoy about your work?"},
        {"role": "user", "content": "I enjoy finding patterns."},
    ]
    assert app.session_state["model"] is model
