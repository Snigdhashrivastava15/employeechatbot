import os
import pandas as pd
from io import StringIO
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.genai as genai
from google.genai.errors import APIError

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash-preview-05-20"
TOP_N_RESULTS = 10

stemmer = PorterStemmer()
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')
    stop_words = set(stopwords.words('english'))


def stem_tokenizer(text):
    tokens = nltk.word_tokenize(text.lower())
    return [
        stemmer.stem(t)
        for t in tokens
        if t.isalpha() and len(t) > 1 and t not in stop_words
    ]


def load_and_index_data(csv_file_path):
    df = pd.read_csv(csv_file_path).fillna("")
    df["Corpus"] = df["EmployeeName"] + " " + df["Work"] + " " + df["Role"] + " " + df["ProjectName"] + " " + df["Action"]
    
    df_clean = df[
        (df['EmployeeName'].str.strip() != '') |
        (df['Work'].str.strip() != '') |
        (df['ProjectName'].str.strip() != '')
    ].reset_index(drop=True)
    
    vectorizer = TfidfVectorizer(tokenizer=stem_tokenizer)
    tfidf_matrix = vectorizer.fit_transform(df_clean["Corpus"])
    
    return df_clean, vectorizer, tfidf_matrix


def retrieve_context(query, df, vectorizer, tfidf_matrix):
    query_vector = vectorizer.transform([query])
    cosine_sim = cosine_similarity(query_vector, tfidf_matrix).flatten()
    indices = cosine_sim.argsort()[-TOP_N_RESULTS:][::-1]

    context = "Relevant Data:\n"
    for _, row in df.iloc[indices].iterrows():
        context += (
            f"- Employee: {row['EmployeeName']} | "
            f"Work: {row['Work']} | "
            f"Project: {row['ProjectName']} | "
            f"Details: {row['Action']}\n"
        )
    return context


def ask_gemini(query, context):
    prompt = f"{context}\n\nUser Question: {query}"
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt]
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"
