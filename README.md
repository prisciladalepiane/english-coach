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

## Para Testar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
python -m pip install "streamlit>=1.48,<2"
python -m pip install "pytest>=8,<10"
```
Rodar o app:

```bash
python -m streamlit run app.py
```

Testes:

```bash
python -m pytest tests/test_app.py -v
```

## Estado atual

Interface de chat com historico, configuracao tipada e download
controlado do GGUF. O modelo ainda nao e carregado na memoria.

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
