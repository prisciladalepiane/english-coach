import streamlit as st


def main() -> None:
    """Renderiza a tela inicial enquanto construimos o projeto."""
    st.set_page_config(page_title="English Conversation Coach", page_icon="💬")
    st.title("English Conversation Coach")
    st.info("Passo 1 concluido: a estrutura do projeto esta pronta.")


if __name__ == "__main__":
    main()
