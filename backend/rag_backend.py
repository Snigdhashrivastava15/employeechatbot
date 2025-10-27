import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_and_index_data(csv_path):
    df = pd.read_csv(csv_path)

    df["combined"] = df["EmployeeName"].astype(str) + " " + \
                     df["ProjectName"].astype(str) + " " + \
                     df["Work"].astype(str)

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(df["combined"])
    return df, vectorizer, matrix


def search(query, df, vectorizer, matrix):
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, matrix)
    idx = similarity.argmax()

    result = df.iloc[idx]
    return f"""
Employee: {result['EmployeeName']}
Project: {result['ProjectName']}
Task/Work: {result['Work']}
"""
