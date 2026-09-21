from pathlib import Path

import streamlit as st

from english_coach.config import ConfigError, Settings, load_settings


SETTINGS_PATH = Path(__file__).resolve().parent / "config" / "settings.yaml"

WELCOME_MESSAGE = (
    "Hi! I'm your English conversation partner. "
    "What would you like to talk about?"
)


def initialize_chat() -> None:
    """Cria o historico somente na primeira execucao da sessao."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]


def render_history() -> None:
    """Exibe novamente todas as mensagens armazenadas na sessao."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def create_mock_response() -> str:
    """Resposta temporária enquanto o modelo não foi conectado."""
    return "**Chat:** Okay, let's talk about that!"


def render_sidebar(settings: Settings) -> None:
    """Mostra a configuracao de inferencia selecionada."""
    with st.sidebar:
        st.subheader("Runtime configuration")
        st.write(f"Model: `{settings.model.repository}`")
        st.write(f"Quantization: `{settings.model.quantization}`")
        st.write(f"Context: `{settings.model.context_size}` tokens")


def main() -> None:
    """Renderiza a interface de conversa."""

    try:
        settings = load_settings(SETTINGS_PATH)
    except ConfigError as error:
        st.error(str(error))
        st.stop()

    st.set_page_config(page_title=settings.application.name, page_icon="💬")
    st.title(settings.application.name)
    st.caption("English practice · Local model coming in the next steps")
    render_sidebar(settings)
    initialize_chat()
    render_history()

    if prompt := st.chat_input("Write your answer in English"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = create_mock_response()
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == "__main__":
    main()
