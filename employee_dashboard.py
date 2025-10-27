import os
import streamlit as st
import pandas as pd
from io import StringIO
import re
import json 
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.genai as genai
from google.genai.errors import APIError

# --- 1. CONFIGURATION & INITIAL SETUP ---

GEMINI_API_KEY = "AIzaSyAWJbaYVCpiHUYazPacXPcqRZqSWEzXDT0" 
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

MODEL_NAME = "gemini-2.5-flash-preview-05-20"
TOP_N_RESULTS = 10 

UPLOADED_CSV_CONTENT = """EmployeeName,Work,Role,ProjectName,Action
Abhishek,Email Archival,Check if organisational permission required & run test on business email on the model  ,Regent,
Avni,OCR for hand written & pdf bills,,OCR/ regent,
Gaurav Sir,,,Taggd,
Param,Internal AI Chatbot,Streaming response & timeout issue solved,CK Birla,
Param,,,Mymudra,Pinnacle support details received
Param,,,Tataplay,
Param,Subtitle/speech dubbing,,OTT/Naveen,Check AWS Polly by Param
Pratham,Vehicle number detection from photograph,API setup for POC,,
Pratham,Create Groupchat & share analysis on intent of exchanged messages in group chat.,Pratham to discuss the flow with Gaurav Sir on monday,Groome,Share architecture by Gaurav sir
Shubh Sir,Talktrack,Price of model required,,
Vanshika,"Competetive price, Scrapping to be done ",Amazon & Flipkart scrapping done. Ajio is pending,Cocoblu,Customer demo done. Monday for followup with Rajat Sir
Vanshika,Cloud Architecture Management,Cloud Architecture diagram & AWS cost to be sent by Vanshika,Gupio,Monday meeting
Vanshika,Cloud Architecture Management,Prepare optimised Cloud architecture and cost ,TitanEd,
Vanshika, Onboarding Voice Bot to AWS,Account login required from client,Cherrymind,
,Call recording analysis proposal,,Rajasthan police,Sample recording to be taken from Rajasthan police. (Ask dinesh Sir )
,,,Healthians,
,AWS Optemisation,,Mindgate,
,AWS Optemisation,,Hero homes,
,Data Migration,,Digital Classroom,
,,,
,,,
"""

# Initialize Stemmer and Stopwords globally
stemmer = PorterStemmer()
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('punkt', quiet=True)


# --- 2. NLP PIPELINE (Tokenization, Stemming, Vectorization) ---

def stem_tokenizer(text):
    """Custom tokenizer that performs tokenization, stop word removal, and stemming."""
    tokens = nltk.word_tokenize(text.lower())
    processed_tokens = [
        stemmer.stem(token) 
        for token in tokens 
        if token.isalpha() and len(token) > 1 and token not in stop_words
    ]
    return processed_tokens

@st.cache_resource
def load_and_index_data(csv_string):
    """
    Loads CSV data, preprocesses it, and creates the TF-IDF index.
    """
    # 1. Load Data and initial cleanup
    df = pd.read_csv(StringIO(csv_string))
    df = df.fillna('')
    
    # 2. Define Corpus and Aggressive Cleanup
    df['Corpus'] = df['EmployeeName'] + ' ' + df['Work'] + ' ' + df['Role'] + ' ' + df['ProjectName'] + ' ' + df['Action']
    
    # Filter rows that are entirely empty across key columns
    df_clean = df[
        (df['EmployeeName'].str.strip() != '') | 
        (df['Work'].str.strip() != '') |
        (df['ProjectName'].str.strip() != '')
    ].reset_index(drop=True)
    
    if df_clean.empty:
        raise ValueError("The provided CSV data is empty or could not be processed after cleaning.")

    # 3. Create Vectorizer 
    tfidf_vectorizer = TfidfVectorizer(
        tokenizer=stem_tokenizer,
        stop_words=list(stop_words)
    )
    
    # 4. Fit and Transform on the CLEANED data
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_clean['Corpus'])
    
    return df_clean, tfidf_vectorizer, tfidf_matrix

# Load resources upon app startup
try:
    data_df, vectorizer, tfidf_matrix = load_and_index_data(UPLOADED_CSV_CONTENT)
except ValueError as e:
    st.error(f"Data Initialization Error: {e}")
    st.stop()
except Exception as e:
    st.error(f"An error occurred during resource loading. Please check the API key and NLTK setup. Error: {e}")
    st.stop()


# --- 3. RETRIEVAL FUNCTION ---

def retrieve_context(query, df, vectorizer, tfidf_matrix):
    """Finds the most relevant rows from the DataFrame based on the query."""
    query_vector = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-TOP_N_RESULTS-1:-1]
    relevant_data = df.iloc[related_docs_indices]
    
    # Format the relevant data as a string
    context_string = "--- Relevant Data from Project CSV ---\n"
    for _, row in relevant_data.iterrows():
        clean_row = {k: v for k, v in row.items() if v != '' and k not in ['Corpus']}
        context_string += f"Employee: {clean_row.get('EmployeeName', 'N/A')}, Work/Task: {clean_row.get('Work', 'N/A')}, Project: {clean_row.get('ProjectName', 'N/A')}, Details: {clean_row.get('Action', 'N/A')}, Role: {clean_row.get('Role', 'N/A')}\n"
    
    context_string += "--------------------------------------\n"
    return context_string

# --- 4. GEMINI GENERATION FUNCTION (Non-Streaming) ---

def ask_gemini(query, context):
    """
    Sends the context and query to the Gemini model for a final, non-streaming answer.
    """
    
    system_prompt = (
        "You are an Employee Project Management Chatbot. Your primary role is to act "
        "as a highly efficient assistant to answer questions about ongoing projects, "
        "employee tasks, and project details based ONLY on the provided relevant data. "
        "Keep your response concise, professional, and directly address the user's question. "
        "If the data does not contain the answer, state clearly that the information is not available in the current project records."
    )
    
    user_prompt = f"{context}\n\nUSER QUESTION: {query}"
    
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Use generate_content for a single, non-streaming response
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[user_prompt],
            config={
                "system_instruction": system_prompt
            }
        )
        return response.text
    except APIError as e:
        error_details = e.args[0]
        message = "Unknown API Error"
        code = 500
        
        if isinstance(error_details, dict):
            try:
                message = error_details['error']['message']
                code = error_details['error']['code']
            except KeyError:
                message = "API error structure invalid. See console for details."
        elif isinstance(error_details, str):
            message = error_details
            if 'API key not valid' in message:
                code = 400
        
        if code == 400 or 'API key not valid' in message:
             return "⛔️ **API Key Error:** The Gemini API key configured in the script is invalid."
        else:
             return f"Sorry, I encountered an API error (Code: {code}). Details: {message}"
    except Exception as e:
        return f"An unexpected Python error occurred: {e}"

# --- 5. STREAMLIT APP ---

def main():
    """Main Streamlit application logic."""
    st.set_page_config(page_title="Employee Chatbot", layout="wide")

    st.title("👨‍💼 Employee Project Chatbot")
    st.caption("Now using a **non-streaming** method to ensure environment stability.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your Project Management assistant. I can answer questions about employee tasks and projects."}
        ]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask about an employee, task, or project..."):
        # 1. Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Process and get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base and generating response..."):
                # a. Retrieval step
                context = retrieve_context(prompt, data_df, vectorizer, tfidf_matrix)
                
                # --- DEBUGGING STEP ---
                print("RAG Context sent to LLM:\n", context)
                # -----------------------

                # b. Generation step (using the non-streaming function)
                full_response = ask_gemini(prompt, context)
                
                # c. Display full response immediately
                st.markdown(full_response if full_response else "*(API returned no text. Check terminal for RAG Context details.)*")
        
        # 3. Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
