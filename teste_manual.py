
from pathlib import Path
from llama_cpp import Llama


MODEL_PATH = Path("models/Qwen3-4B-Q4_K_M.gguf")
PROMPT_PATH = Path("prompts/system_prompt.txt")

system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

llm = Llama(
    model_path=str(MODEL_PATH),
    n_ctx=2048,
    verbose=False,
)

response = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": f"{system_prompt}\n/no_think",
        },
        {
            "role": "user",
            "content": "I work with data analysis and I want to improve my English.",
        },
    ],
    temperature=0.7,
    top_p=0.8,
    max_tokens=120,
)

message = response["choices"][0]["message"]["content"]
print(message)