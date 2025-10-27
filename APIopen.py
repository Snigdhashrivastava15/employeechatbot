import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os
from transformers import pipeline

# -------------------------------
# CONFIGURATION
# -------------------------------

# Excel file path
EXCEL_PATH = r"C:\Users\SNIGDHA\OneDrive\Desktop\Employee System\Internal Ongoing Project Discussion _ Gaurav Sir .xlsx"

# Firebase credentials path
FIREBASE_CRED_PATH = r"C:\Users\SNIGDHA\OneDrive\Desktop\Employee System\firebase-adminsdk-abc123-def456.json"

# Initialize Firebase
firebase_initialized = False
if os.path.exists(FIREBASE_CRED_PATH):
    try:
        cred = credentials.Certificate(FIREBASE_CRED_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        firebase_initialized = True
        st.sidebar.success("Firebase connected successfully")
    except Exception as e:
        st.sidebar.error(f"Firebase initialization failed: {e}")
else:
    st.sidebar.warning("Firebase credentials not found. Some features will be disabled.")

# -------------------------------
# LOAD EXCEL DATA
# -------------------------------
@st.cache_data
def load_excel_data():
    if not os.path.exists(EXCEL_PATH):
        st.error(f"Excel file not found at {EXCEL_PATH}")
        return pd.DataFrame()
    try:
        df = pd.read_excel(EXCEL_PATH)
        df = df.rename(columns={
            "Person Assigned": "EmployeeName",
            "Procedure/ Error": "Role",
            "Use Case": "Work",
            "Project": "ProjectName"
        })
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return pd.DataFrame()

# -------------------------------
# FIREBASE OPERATIONS
# -------------------------------
def upload_to_firebase(df):
    if not firebase_initialized:
        st.error("Firebase not initialized. Cannot upload data.")
        return
    for _, row in df.iterrows():
        doc_ref = db.collection("employees").document(row["EmployeeName"])
        doc_ref.set(row.to_dict())

def fetch_from_firebase():
    if not firebase_initialized:
        st.error("Firebase not initialized. Cannot fetch data.")
        return pd.DataFrame()
    docs = db.collection("employees").stream()
    data = [doc.to_dict() for doc in docs]
    return pd.DataFrame(data)

def add_record(record):
    if firebase_initialized:
        db.collection("employees").add(record)

def update_record(employee_name, updated_data):
    if firebase_initialized:
        docs = db.collection("employees").where("EmployeeName", "==", employee_name).stream()
        for doc in docs:
            db.collection("employees").document(doc.id).update(updated_data)

def delete_record(employee_name):
    if firebase_initialized:
        docs = db.collection("employees").where("EmployeeName", "==", employee_name).stream()
        for doc in docs:
            db.collection("employees"].document(doc.id).delete()

# -------------------------------
# HUGGING FACE CHATBOT
# -------------------------------
@st.cache_resource
def load_hf_model():
    return pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")

hf_model = load_hf_model()

def chatbot_query(prompt):
    try:
        result = hf_model(prompt, max_length=150, do_sample=True, temperature=0.7)
        return result[0]['generated_text']
    except Exception as e:
        return f"Error: {e}"

# -------------------------------
# STREAMLIT DASHBOARD
# -------------------------------
st.set_page_config(page_title="Employee Management Dashboard", layout="wide")
st.title("Employee Management Dashboard")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Upload Data", "View Dashboard", "Add Employee", "Update Employee", "Delete Employee", "Chatbot"]
)

# Upload Excel → Firebase
if menu == "Upload Data":
    st.header("Upload Excel Data to Firebase")
    df = load_excel_data()
    if not df.empty:
        st.dataframe(df)
        if st.button("Upload to Firebase"):
            upload_to_firebase(df)
            st.success("Data uploaded to Firebase successfully!")

# View Dashboard
elif menu == "View Dashboard":
    st.header("Employee Data")
    data = fetch_from_firebase() if firebase_initialized else pd.DataFrame()
    if not data.empty:
        employee_filter = st.selectbox("Filter by Employee", ["All"] + sorted(data["EmployeeName"].unique()))
        project_filter = st.selectbox("Filter by Project", ["All"] + sorted(data["ProjectName"].unique()))
        role_filter = st.selectbox("Filter by Role", ["All"] + sorted(data["Role"].unique()))

        filtered_data = data.copy()
        if employee_filter != "All":
            filtered_data = filtered_data[filtered_data["EmployeeName"] == employee_filter]
        if project_filter != "All":
            filtered_data = filtered_data[filtered_data["ProjectName"] == project_filter]
        if role_filter != "All":
            filtered_data = filtered_data[filtered_data["Role"] == role_filter]

        st.dataframe(filtered_data)
    else:
        st.warning("No data found in Firebase.")

# Add Employee
elif menu == "Add Employee":
    st.header("Add New Employee Record")
    with st.form("add_form"):
        employee = st.text_input("Employee Name")
        work = st.text_input("Work (Use Case)")
        role = st.text_input("Role (Procedure/Error)")
        project = st.text_input("Project Name")
        action = st.text_input("Action Required")
        submitted = st.form_submit_button("Add Record")
        if submitted and employee and work:
            record = {"EmployeeName": employee, "Work": work, "Role": role, "ProjectName": project, "Action": action}
            add_record(record)
            st.success("Record added successfully!")

# Update Employee
elif menu == "Update Employee":
    st.header("Update Employee Record")
    name = st.text_input("Enter Employee Name to Update")
    updated_role = st.text_input("New Role")
    updated_project = st.text_input("New Project Name")
    updated_action = st.text_input("New Action")
    if st.button("Update"):
        update_record(name, {"Role": updated_role, "ProjectName": updated_project, "Action": updated_action})
        st.success("Employee record updated successfully!")

# Delete Employee
elif menu == "Delete Employee":
    st.header("Delete Employee Record")
    name = st.text_input("Enter Employee Name to Delete")
    if st.button("Delete"):
        delete_record(name)
        st.success("Record deleted successfully!")

# Chatbot
elif menu == "Chatbot":
    st.header("Chat with Dashboard")
    prompt = st.text_input("Ask something (e.g., 'Show all tasks assigned to Snigdha')")
    if st.button("Ask"):
        if prompt:
            result = chatbot_query(prompt)
            st.write(result)
        else:
            st.warning("Please enter a question.")
