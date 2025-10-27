import streamlit as st
from backend.rag_backend import load_and_index_data, search

CSV_PATH = "data/project_data.csv"

st.title("Employee Project Lookup Chatbot ")

@st.cache_resource
def load_data():
    return load_and_index_data(CSV_PATH)

df, vectorizer, matrix = load_data()

query = st.text_input("Ask about employee or work:")

if st.button("Search"):
    if query.strip():
        response = search(query, df, vectorizer, matrix)
        st.success(response)
    else:
        st.warning("Please enter a query!")
