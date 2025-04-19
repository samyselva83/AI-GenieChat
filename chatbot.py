import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
#from langchain_groq import ChatGroq
import streamlit as st

def main():
    # ✅ Load environment variables
    load_dotenv()
    
    # ✅ Get API Key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found. Please set it in your .env file.")
        return

    # ✅ Create LLM object
    llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    model="HuggingFaceH4/zephyr-7b-beta"
    )
    #llm = ChatGroq(
    #    model="llama3-70b-8192",
    #    temperature=0.7,
    #    api_key=api_key
    #)

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
        with st.chat_message("user" ,avatar="👤"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input, "avatar": "👤"})

        # System instruction
        system_msg = {
            "role": "system",
            "content": "You are a helpful assistant who helps to answer user queries clearly and concisely."
        }

        # Build the full prompt
        prompt = [system_msg]
        for msg in st.session_state.chat_history:
            prompt.append({"role": msg["role"].lower(), "content": msg["content"]})
        prompt.append({"role": "user", "content": user_input , "avatar": "👤"})

        # Call LLM
        try:
            response = llm.invoke(prompt)
            answer = response.content
        except Exception as e:
            answer = f"⚠️ Error: {e}"
        
        with st.chat_message("assistant",avatar="🤖"):
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "avatar": "🤖"})
        

# ✅ Entry point protection
if __name__ == "__main__":
    main()
