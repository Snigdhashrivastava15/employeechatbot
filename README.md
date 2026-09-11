# 🤖 Company Chatbot — GenAI Workflow Automation Platform

An **LLM-powered enterprise chatbot and agentic workflow automation platform** designed to automate internal business operations, answer employee queries using **Retrieval-Augmented Generation (RAG)**, and execute multi-step tasks through **tool calling and MCP integrations**.

The platform combines **GenAI, RAG, agentic workflows, Python, Flask, AWS, data pipelines, and CI/CD** to create a scalable and reliable enterprise automation solution.

> **Key impact:** Automated workflows reduced average handling time (AHT) by approximately **30%**.

---

## 🚀 Overview

The Company Chatbot is designed to go beyond traditional question-answering systems.

Instead of simply generating a response, the system can:

* Understand incoming business requests
* Classify user intent
* Retrieve relevant information from enterprise data
* Generate grounded responses using RAG
* Call external tools and APIs
* Execute multi-step workflows
* Validate generated responses
* Abstain from answering when confidence is low
* Route unresolved requests to fallback or human workflows

The system is designed around an **agentic orchestration layer** that coordinates LLM reasoning, retrieval, tools, and external integrations.

---

## 🎯 Key Results

| Metric                   | Result                                   |
| ------------------------ | ---------------------------------------- |
| Average Handling Time    | **~30% reduction**                       |
| Workflow Automation      | Reduced manual intervention              |
| Hallucination Risk       | Reduced using RAG and correctness checks |
| Low-Confidence Responses | Handled using abstention/fallback logic  |
| Deployment               | Automated CI/CD using GitHub Actions     |

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────────┐
                         │     User Request         │
                         │ Chat / Email / Ticket    │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │ Intent Router / Agent    │
                         │      Orchestrator        │
                         └────────────┬─────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
       ┌─────────────┐        ┌──────────────┐        ┌─────────────┐
       │     LLM     │        │     RAG      │        │ Tool Calling│
       │  Reasoning  │        │  Retrieval   │        │ / Functions │
       └──────┬──────┘        └──────┬───────┘        └──────┬──────┘
              │                       │                       │
              └───────────────────────┼───────────────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │      MCP Integrations   │
                         │ External APIs / Systems  │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │ Correctness & Confidence │
                         │ Checks / Abstention      │
                         └────────────┬─────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
                 ┌──────────────┐         ┌────────────────┐
                 │   Response   │         │ Fallback /     │
                 │   to User    │         │ Human Review   │
                 └──────────────┘         └────────────────┘
```

### Data Pipeline

```text
Raw Enterprise Data
        │
        ▼
PySpark / Pandas ETL
        │
        ▼
Data Cleaning & Normalisation
        │
        ├───────────────┐
        ▼               ▼
   Databricks        Snowflake
        │               │
        └───────┬───────┘
                ▼
        Retrieval / Feature
             Pipeline
                │
                ▼
          RAG + LLM Layer
```

### AWS Deployment

```text
GitHub Repository
       │
       ▼
GitHub Actions
       │
       ├── Tests
       ├── Validation
       └── Build
       │
       ▼
Docker Image
       │
       ▼
Amazon ECR
       │
       ▼
Amazon EC2
       │
       ▼
Flask REST API
       │
       ▼
GenAI / RAG / Agentic Services
```

---

# ✨ Core Features

## 1. Agentic Workflow Orchestration

The chatbot can interpret a request and execute multiple steps instead of returning a simple text response.

Example:

```text
User Request
     ↓
Classify Intent
     ↓
Retrieve Context
     ↓
Call Required Tool
     ↓
Process Result
     ↓
Validate Output
     ↓
Return Response
```

This enables automation of multi-step business workflows.

---

## 2. Retrieval-Augmented Generation

The system uses RAG to ground LLM responses in enterprise data.

```text
User Query
    ↓
Query Processing
    ↓
Retriever
    ↓
Relevant Documents
    ↓
Context Construction
    ↓
LLM
    ↓
Grounded Response
```

RAG helps reduce hallucinations by providing the model with relevant business information before generation.

---

## 3. MCP Integrations

The platform supports **Model Context Protocol (MCP)** integrations for connecting the agent with external tools and services.

This allows the system to interact with downstream systems rather than only generating text.

---

## 4. Tool / Function Calling

The agent can determine when an external tool is required and invoke the appropriate function.

Example:

```text
User:
"Process the pending invoice for vendor XYZ."

Agent
   ↓
Identify required action
   ↓
Call ERP tool
   ↓
Process invoice
   ↓
Update ticket
   ↓
Return confirmation
```

---

## 5. Correctness Checks

Generated responses are evaluated before being returned to the user.

The system checks:

* Response confidence
* Expected output patterns
* Retrieved context
* Tool execution status
* Potentially incorrect responses

---

## 6. Abstention & Fallback Handling

When the system is not sufficiently confident, it can avoid returning an unreliable answer.

```text
LLM Response
      ↓
Confidence Check
      │
 ┌────┴─────┐
 │          │
 ▼          ▼
High      Low
 │          │
 ▼          ▼
Return    Abstain
Answer      │
            ▼
       Fallback / Human
          Review
```

This approach prioritises **correctness over blindly generating an answer**.

---

# 🛠️ Technology Stack

### GenAI / LLM

* LLM-based application development
* Prompt Engineering
* Agentic Workflows
* Function / Tool Calling
* MCP
* Retrieval-Augmented Generation
* Confidence & Abstention Logic

### Programming

* Python
* Flask
* REST APIs

### Data Engineering

* Pandas
* PySpark
* Databricks
* Snowflake
* ETL Pipelines
* Data Cleaning & Transformation

### Machine Learning / NLP

* TensorFlow
* Keras
* NLP pipelines
* Model serving

### AWS

* Amazon EC2
* Amazon S3
* Amazon VPC
* AWS IAM
* Amazon ECR

### DevOps

* Docker
* Git
* GitHub Actions
* CI/CD
* Automated Testing

---

# 📁 Project Structure

```text
company-chatbot/
│
├── agent/
│   ├── orchestrator.py
│   ├── tools/
│   └── mcp_clients/
│
├── prompts/
│   ├── templates/
│   └── eval/
│
├── pipelines/
│   ├── etl/
│   └── feature_engineering/
│
├── api/
│   ├── app.py
│   ├── models/
│   └── nlp/
│
├── monitoring/
│   ├── confidence_checks.py
│   └── dashboards/
│
├── infra/
│   └── terraform/
│
├── tests/
│
├── requirements.txt
└── README.md
```

> Keep `terraform/` and `cdk/` as separate actual directories if you use both. Do not write `terraform/ or cdk/` as a filesystem path.

---

# ⚙️ Getting Started

## Prerequisites

Make sure the following are installed:

* Python 3.10+
* Git
* AWS CLI
* Docker
* Access to the required AWS resources
* Required LLM API credentials
* Databricks / Snowflake access if using the data pipeline

---

## Clone the Repository

```bash
git clone https://github.com/<your-org>/company-chatbot.git

cd company-chatbot
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Locally

Start the Flask API:

```bash
python api/app.py
```

Run the agent orchestrator:

```bash
python agent/orchestrator.py --dev
```

The API can then be used by your frontend or API client.

---

# 📡 API Reference

## `POST /predict`

Returns a model prediction for a given input.

### Request

```json
{
  "input_text": "Customer requesting refund status for order #12345",
  "context": {
    "channel": "email"
  }
}
```

### Response

```json
{
  "prediction": "refund_status_inquiry",
  "confidence": 0.92,
  "abstained": false
}
```

---

## `POST /agent/run`

Starts an agentic workflow.

### Request

```json
{
  "request": "Please process the pending invoice for vendor XYZ",
  "user_id": "emp-4521"
}
```

### Response

```json
{
  "status": "completed",
  "steps_executed": [
    "classify_request",
    "call_erp_tool",
    "update_ticket"
  ],
  "result": "Invoice processed and vendor notified.",
  "confidence": 0.88
}
```

---

# 🔄 Data Pipeline

The data pipeline follows these major stages:

### 1. Ingestion

Raw enterprise data is collected from internal sources.

### 2. Cleaning

PySpark and Pandas are used for:

* Deduplication
* Normalisation
* Schema enforcement
* Data transformation

### 3. Storage & Processing

Processed data is stored and analysed through:

* Databricks
* Snowflake

### 4. Feature Engineering

Structured data is prepared for:

* RAG retrieval
* Model inputs
* Feature generation

### 5. Serving

The application consumes curated data through the retrieval and API layers.

---

# ☁️ Deployment & CI/CD

The application is deployed using AWS infrastructure.

### Deployment Flow

```text
Developer
   │
   ▼
Git Commit
   │
   ▼
GitHub Repository
   │
   ▼
GitHub Actions
   │
   ├── Unit Tests
   ├── Integration Tests
   ├── Prompt Evaluation
   └── Build
   │
   ▼
Docker Image
   │
   ▼
Amazon ECR
   │
   ▼
Amazon EC2
   │
   ▼
Application
```

GitHub Actions is used to automate testing and deployment workflows.

---

# 🔍 Monitoring & Reliability

The platform includes several mechanisms to improve reliability.

### Correctness Checks

LLM outputs are validated against configured expectations and confidence thresholds.

### Abstention

Low-confidence responses are not blindly returned to users.

Instead, the system can:

```text
Low Confidence
      ↓
Abstain
      ↓
Fallback
      ↓
Human Review / Alternative Workflow
```

### Observability

Important production metrics include:

* Request latency
* Response accuracy
* Abstention rate
* Tool-call success rate
* Workflow completion rate
* Error rate

---

# 🧪 Testing & Evaluation

The platform can evaluate both traditional application behaviour and GenAI-specific behaviour.

### Application Testing

* Unit tests
* Integration tests
* API testing

### GenAI Evaluation

* Prompt regression testing
* Retrieval quality evaluation
* Response correctness
* Confidence evaluation
* Hallucination checks

---

# 📊 Example Workflow

Consider an employee asking:

```text
"What is the status of my current project?"
```

The system can process the request as follows:

```text
User Query
    ↓
Intent Classification
    ↓
Retrieve Employee / Project Data
    ↓
RAG Context Construction
    ↓
LLM Response Generation
    ↓
Confidence Check
    ↓
Response
```

For an action-oriented request:

```text
User Request
    ↓
Intent Router
    ↓
Agent
    ↓
Tool Selection
    ↓
External System / API
    ↓
Result
    ↓
Validation
    ↓
User Response
```

---

# 🗺️ Roadmap

* [ ] Expand MCP integrations
* [ ] Add additional enterprise tools
* [ ] Add automated prompt regression testing
* [ ] Improve confidence threshold optimisation
* [ ] Add richer monitoring dashboards
* [ ] Add continuous evaluation pipelines
* [ ] Add multilingual support
* [ ] Improve workflow failure recovery

---

# 🔐 Security Considerations

The platform is designed to use AWS IAM and controlled access to cloud resources.

Recommended production practices include:

* IAM least-privilege policies
* Environment variables for secrets
* Secure API authentication
* Private networking where appropriate
* Logging and audit trails
* Input validation
* Role-based access control

**Never commit API keys, AWS credentials, passwords, or other secrets to the repository.**

---

# 🤝 Contributing

Contributions are welcome.

```bash
# Create a feature branch
git checkout -b feature/your-feature

# Make your changes
git add .

# Commit
git commit -m "Add your feature"

# Push
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

See [`LICENSE`](LICENSE) for more information.

---

## 👩‍💻 Author

**Snigdha Shrivastava**

GenAI / Cloud Engineer
Python | AWS | RAG | LLMs | Agentic AI | MCP | Docker | CI/CD

### GitHub

[GitHub Profile](https://github.com/Snigdhashrivastava15092003)

---

⭐ If you find this project useful, consider giving it a star.
