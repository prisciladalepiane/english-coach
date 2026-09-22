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

## Executar localmente

Requisito: Python 3.11, 3.12 ou 3.13. Na raiz do projeto, crie e ative um
ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependencias e registre o pacote local em modo editavel:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install --no-deps -e .
```

Inicie o aplicativo:

```bash
python -m streamlit run app.py
```

Abra `http://localhost:8501` no navegador. Se o GGUF ainda nao estiver em
`models/`, use o botao de download na barra lateral.

Execute todos os testes automatizados:

```bash
python -m pytest -v
```

Para conversar diretamente com o modelo pelo terminal:

```bash
python teste_manual.py
```

## Estado atual

Interface de chat com historico, configuracao tipada e download
controlado do GGUF. O modelo ja pode ser testado manualmente, mas ainda nao
esta conectado ao fluxo do Streamlit.

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

## Arquitetura

O projeto separa a interface, as regras da conversa e a execucao do modelo:

```text
Navegador
   |
   v
app.py                    Interface Streamlit
   |
   +--> config.py ------> config/settings.yaml
   |
   +--> chat.py --------> prompts/system_prompt.txt
   |       |
   |       v
   +--> model.py -------> Qwen GGUF em models/
   |
   `--> logging_config.py
```

Principais responsabilidades:

- `app.py`: recebe mensagens, mostra o historico e renderiza a interface;
- `config.py`: le e valida as configuracoes do YAML;
- `chat.py`: organizara o historico e as regras pedagogicas do agente;
- `model.py`: localiza, baixa e executara o modelo GGUF;
- `system_prompt.txt`: define o comportamento do professor de ingles;
- `logging_config.py`: centralizara logs e metricas de execucao;
- `tests/`: testa cada camada sem precisar executar sempre o modelo real.

Atualmente, `app.py` ainda usa uma resposta simulada. A proxima integracao sera:

```text
app.py -> chat.py -> model.py -> Qwen -> resposta
```

A descricao completa, incluindo fluxo das mensagens, estrategia de testes e
estado de cada componente, esta em
[`docs/architecture.md`](docs/architecture.md).

## Modelo planejado

- Repositorio: `Qwen/Qwen3-4B-GGUF`
- Quantizacao inicial: `Q4_K_M`
