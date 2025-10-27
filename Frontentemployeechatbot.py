import streamlit as st
import sys, os

#  Make sure backend is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.rag_backend import load_and_index_data, retrieve_context, ask_gemini

#  Updated CSV path based on your file
CSV_PATH = "Internal Ongoing Project Discussion _ Gaurav Sir .csv"

st.set_page_config(page_title="Employee Project Chatbot", layout="wide")
st.title("👨‍💼 Employee Project Chatbot")
st.caption("Ask about employees, project status, actions, and more ")

# Load CSV once
if "data" not in st.session_state:
    df, vectorizer, matrix = load_and_index_data(CSV_PATH)
    st.session_state.data = (df, vectorizer, matrix)

df, vectorizer, matrix = st.session_state.data

# Chat history
if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# Display chat history
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_query := st.chat_input("Ask something..."):
    st.session_state.chat.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing employee data..."):
            context = retrieve_context(user_query, df, vectorizer, matrix)
            answer = ask_gemini(user_query, context)
            st.write(answer)
            st.session_state.chat.append({"role": "assistant", "content": answer})
