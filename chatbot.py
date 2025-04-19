import os
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceEndpoint
from langchain_groq import ChatGroq
import streamlit as st

def main():
    # ✅ Load environment variables
    load_dotenv()

    huggingface_token = os.getenv("Huggingkey_new_token")
    groq_api_key = os.getenv("GROQ_API_KEY")

    # ✅ Streamlit UI
    st.title("🤖 GenieChat\n\nYour AI assistant — by Selvakumar")

    model_choice = st.radio("Choose your LLM provider:", ("HuggingFace", "Groq"))

    # ✅ Create LLM object based on choice
    if model_choice == "HuggingFace":
        if not huggingface_token:
            st.error("HuggingFace token not found.")
            return
        llm = HuggingFaceEndpoint(
            repo_id="google/flan-t5-large",  # Make sure it supports 'text2text-generation'
            task="text2text-generation",
            huggingfacehub_api_token=huggingface_token
        )
    else:
        if not groq_api_key:
            st.error("GROQ_API_KEY not found.")
            return
        llm = ChatGroq(
            model="llama3-70b-8192",
            api_key=groq_api_key,
            temperature=0.7
        )

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"], avatar=chat.get("avatar", "👤")):
            st.markdown(chat["content"])

    if user_input := st.chat_input("Ask something..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input, "avatar": "👤"})

        try:
            if model_choice == "HuggingFace":
                answer = llm.invoke(user_input)
            else:
                answer = llm.invoke(user_input).content
        except Exception as e:
            answer = f"⚠️ Error: {e}"

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "avatar": "🤖"})

if __name__ == "__main__":
    main()
