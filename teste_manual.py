from pathlib import Path

from english_coach.config import load_settings


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


if __name__ == "__main__":
    main()