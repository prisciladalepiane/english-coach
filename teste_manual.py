from pathlib import Path
from llama_cpp import Llama

from english_coach.config import load_settings
from english_coach.model import generate_response, get_local_model_path
from english_coach.chat import reply


PROJECT_ROOT = Path(__file__).resolve().parent
MODELS_DIR = PROJECT_ROOT / "models"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "system_prompt.txt"
SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yaml"


def main() -> None:
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Models directory: {MODELS_DIR}")
    print(f"Prompts path: {PROMPT_PATH}")
    print(f"Settings path: {SETTINGS_PATH}")

    settings = load_settings(SETTINGS_PATH)
    print(settings)
    print(settings.application)
    print(settings.generation)
    print(settings.model)

    model_path = get_local_model_path(settings.model, MODELS_DIR)
    print(f"Model path: {model_path}")

    model = Llama(
        model_path=str(model_path),
        n_ctx=settings.model.context_size,
        verbose=False,
    )

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8").strip()
    user_message = "Can you help me with my English homework?"
    history = []

    messages = [
        {"role": "system", "content": f"{system_prompt}\n/no_think"},
        *history,
        {"role": "user", "content": user_message},
    ]

    resp = generate_response(model, messages, settings.generation)

    print("Response:", resp)

    reply_resp = reply(model, history, user_message, settings.generation, PROMPT_PATH)
    print("Reply Response:", reply_resp)

if __name__ == "__main__":
    main()
