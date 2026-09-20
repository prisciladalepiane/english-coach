import streamlit as st


WELCOME_MESSAGE = (
    "Hi! I'm your English conversation partner. "
    "What do you what to talk about?"
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
    return (
        "**Chat:** Ok!, Let's talk about that!"
    )

def main() -> None:
    """Renderiza a interface de conversa."""
    
    st.set_page_config(page_title="English Conversation Coach", page_icon="💬")
    
    st.title("English Conversation Coach")
    st.caption("English practice · Local model coming in the next steps")
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
