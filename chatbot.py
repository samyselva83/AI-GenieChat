import streamlit as st
from langchain_groq import ChatGroq
import datetime
import requests

# ✅ Helper: Get user IP address
def get_user_ip():
    try:
        ip = requests.get("https://api.ipify.org").text
    except:
        ip = "Unknown"
    return ip

# ✅ Helper: Log access
def log_access(query):
    ip = get_user_ip()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("access_log.txt", "a") as f:
        f.write(f"{timestamp} | IP: {ip} | Query: {query}\n")

def main():
    # ✅ Get API Key from Streamlit Secrets
    api_key = st.secrets["groq"]["GROQ_API_KEY"]

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

        # ✅ Log the query
        log_access(user_input)

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
