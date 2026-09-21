from pathlib import Path

from llama_cpp import Llama


MODEL_PATH = Path("models/Qwen3-4B-Q4_K_M.gguf")
PROMPT_PATH = Path("prompts/system_prompt.txt")

def main() -> None:
    """Inicia uma conversa interativa com o modelo no terminal."""
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Modelo nao encontrado: {MODEL_PATH}")

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    print("Carregando o modelo...")
    llm = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=2048,
        verbose=False,
    )

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

        response = llm.create_chat_completion(
            messages=messages,
            temperature=0.7,
            top_p=0.8,
            max_tokens=120,
        )

        assistant_message = response["choices"][0]["message"]["content"]
        if not assistant_message:
            assistant_message = "I could not generate a response. Please try again."

        print(f"\nCoach: {assistant_message}\n")
        messages.append({"role": "assistant", "content": assistant_message})


if __name__ == "__main__":
    main()
