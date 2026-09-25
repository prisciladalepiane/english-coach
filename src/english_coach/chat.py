"""Prepara a conversa enviada ao modelo e trata a resposta."""

import re
from pathlib import Path

from llama_cpp import Llama

from english_coach.config import GenerationSettings
from english_coach.model import ModelInferenceError, generate_response


def reply(
    model: Llama,
    history: list[dict[str, str]],
    user_message: str,
    settings: GenerationSettings,
    prompt_path: str | Path,
) -> str:
    """Envia o historico e a nova mensagem ao Qwen."""
    system_prompt = Path(prompt_path).read_text(encoding="utf-8").strip()
    messages = [
        {"role": "system", "content": f"{system_prompt}\n/no_think"},
        *history,
        {"role": "user", "content": user_message},
    ]

    response = generate_response(model, messages, settings)
    response = re.sub(r"<think>.*?</think>\s*", "", response, flags=re.DOTALL)
    response = response.strip()

    return response
