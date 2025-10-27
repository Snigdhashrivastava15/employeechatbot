import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import os

#  Set Gemini API Key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#  Load and index employee data
def load_and_index_data(csv_path):
    df = pd.read_csv(csv_path)
    df["combined"] = df["EmployeeName"] + " " + df["ProjectName"] + " " + df["TaskStatus"]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(df["combined"])
    return df, vectorizer, matrix

#  Retrieve matching employee records based on user query
def retrieve_context(query, df, vectorizer, matrix):
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, matrix)
    top_indices = similarity.argsort()[0][-3:][::-1]
    return df.iloc[top_indices].to_string(index=False)

#  Ask Gemini using the selected context
def ask_gemini(query, context):
    prompt = f"Question: {query}\n\nRelevant Employee Data:\n{context}\n\nProvide a clear answer:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
