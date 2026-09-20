# English Conversation Coach


Projeto educacional para construir, passo a passo, um parceiro de conversacao
em ingles para estudantes de nivel B1. A aplicacao usara:

- Qwen3-4B no formato GGUF;
- `llama.cpp` por meio de Python;
- Streamlit para a interface;
- praticas de MLOps/LLMOps para reproducibilidade, testes e observabilidade.

O agente conversara sobre situacoes cotidianas.
 A cada resposta do estudante, corrigira somente o erro mais
importante, apresentara uma explicacao breve em portugues e fara uma pergunta
natural de continuacao.

## Para Testar

```cmd
python3 -m venv .venv
source .venv/bin/activate

python -m pip install "streamlit>=1.48,<2"
python -m streamlit run app.py
```

## Estado atual

Passo 2: interface de chat com historico de sessao e resposta simulada. O
modelo ainda nao e carregado.

## Estrutura

```text
app.py                 Interface Streamlit
config/                Parametros versionados
prompts/               Instrucoes enviadas ao modelo
src/english_coach/     Logica da aplicacao
tests/                  Testes automatizados
data/                   Dados locais, fora do Git
models/                 Pesos do modelo, fora do Git
```

## Modelo planejado

- Repositorio: `Qwen/Qwen3-4B-GGUF`
- Quantizacao inicial: `Q4_K_M`
