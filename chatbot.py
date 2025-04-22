import streamlit as st
from langchain_groq import ChatGroq

def main():
    # ✅ Get API Key from Streamlit Secrets
    api_key = st.secrets["groq"]["api_key"]

    # ✅ Create LLM object
    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.7,
        api_key=api_key
    )

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

        # System message
        system_msg = {
            "role": "system",
            "content": "You are a helpful assistant who answers clearly and concisely."
        }

        # Build prompt
        prompt = [system_msg] + [
            {"role": msg["role"].lower(), "content": msg["content"]}
            for msg in st.session_state.chat_history
        ]

        # Call LLM
        try:
            response = llm.invoke(prompt)
            answer = response.content
        except Exception as e:
            answer = f"⚠️ Error: {e}"

        # Display bot response
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "avatar": "🤖"})

if __name__ == "__main__":
    main()
