"""Testes das mensagens enviadas ao modelo."""

from pathlib import Path

from english_coach.chat import reply
from english_coach.config import GenerationSettings


def test_reply_uses_prompt_history_and_removes_thinking(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prompt_path = tmp_path / "system_prompt.txt"
    prompt_path.write_text("Act as an English coach.", encoding="utf-8")
    history = [{"role": "assistant", "content": "Hello!"}]
    captured_messages: list[dict[str, str]] = []

    def fake_generate_response(model, messages, settings):
        captured_messages.extend(messages)
        return "<think>Internal text</think>\nYour sentence is clear. What do you do?"

    monkeypatch.setattr("english_coach.chat.generate_response", fake_generate_response)

    response = reply(
        model=object(),
        history=history,
        user_message="I work with data.",
        settings=GenerationSettings(temperature=0.7, top_p=0.8, max_tokens=120),
        prompt_path=prompt_path,
    )

    assert captured_messages == [
        {"role": "system", "content": "Act as an English coach.\n/no_think"},
        {"role": "assistant", "content": "Hello!"},
        {"role": "user", "content": "I work with data."},
    ]
    assert response == "Your sentence is clear. What do you do?"
