import os
import requests
import streamlit as st
from dotenv import load_dotenv

def main():
    # ✅ Load environment variables
    load_dotenv()

    # ✅ Get API Key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found. Please set it in your .env file.")
        return

    # ✅ Streamlit UI
    st.title("🤖 GenieChat\n\nYour AI assistant — by Selvakumar")

    # Setup session history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display previous messages
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"], avatar=chat.get("avatar", "👤")):
            st.markdown(chat["content"])

    # User input
    if user_input := st.chat_input("Ask something..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input, "avatar": "👤"})

        # Prepare the prompt
        messages = [
            {"role": "system", "content": "You are a helpful assistant who helps to answer user queries clearly and concisely."}
        ] + [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.chat_history]

        # Send request to OpenRouter API
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3-70b-instruct",
                    "messages": messages
                }
            )

            if response.status_code == 200:
                answer = response.json()['choices'][0]['message']['content']
            else:
                answer = f"⚠️ Error: {response.text}"
        except Exception as e:
            answer = f"⚠️ Exception: {e}"

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "avatar": "🤖"})


# ✅ Entry point protection
if __name__ == "__main__":
    main()
