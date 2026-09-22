from pathlib import Path

from english_coach.config import load_settings
from english_coach.model import generate_response, load_model


PROJECT_ROOT = Path(__file__).resolve().parent
MODELS_DIR = PROJECT_ROOT / "models"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "system_prompt.txt"
SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yaml"


def main() -> None:
    """Inicia uma conversa interativa com o modelo no terminal."""
    settings = load_settings(SETTINGS_PATH)
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    print("Carregando o modelo...")
    model = load_model(settings.model, MODELS_DIR)

    messages = [
        {
            "role": "system",
            "content": f"{system_prompt}\n/no_think",
        }
    ]

    print("Modelo pronto. Escreva em ingles ou digite 'sair' para encerrar.\n")

    while True:
        try:
            user_message = input("Voce: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nConversa encerrada.")
            break

        if user_message.lower() in {"sair", "exit", "quit"}:
            print("Conversa encerrada.")
            break

        if not user_message:
            continue

        messages.append({"role": "user", "content": user_message})

        assistant_message = generate_response(
            model,
            messages,
            settings.generation,
        )

        print(f"\nCoach: {assistant_message}\n")
        messages.append({"role": "assistant", "content": assistant_message})


if __name__ == "__main__":
    main()
