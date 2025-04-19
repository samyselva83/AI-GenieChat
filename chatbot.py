import os
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceEndpoint
import streamlit as st

def main():
    # ✅ Load environment variables
    load_dotenv()
    
    # ✅ Get Hugging Face API Key
    api_key = os.getenv("Huggingkey_new_token")
    if not api_key:
        st.error("Huggingkey_new_token not found. Please set it in your .env file.")
        return

    # ✅ Create LLM instance
    try:
        llm = HuggingFaceEndpoint(
            repo_id="google/flan-t5-large",
            task="text2text-generation",
            huggingfacehub_api_token=api_key
        )
    except Exception as e:
        st.error(f"⚠️ LLM Initialization Error: {e}")
        return

    # ✅ Streamlit UI
    st.title("🤖 GenieChat\n\nYour AI assistant — by Selvakumar")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display previous messages
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"], avatar=chat.get("avatar", "👤")):
            st.markdown(chat["content"])

    # Input from user
    if user_input := st.chat_input("Ask something..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input, "avatar": "👤"})

        try:
            # Only pass raw string
            response = llm.invoke(user_input)
            answer = response
        except Exception as e:
            answer = f"⚠️ Error: {e}"

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "avatar": "🤖"})

if __name__ == "__main__":
    main()
