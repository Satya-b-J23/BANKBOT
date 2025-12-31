# 🏦 BankBot AI – Banking Chatbot using Ollama

BankBot AI is a domain-specific AI-powered banking chatbot designed to answer
only banking-related queries such as accounts, loans, ATM services, and transactions.
The project uses a local Large Language Model (LLM) through Ollama and a Streamlit-based
web interface.

---

## 🚀 Features

- Banking-only query handling
- Domain restriction & intent filtering
- Polite greeting handling
- Chat history support (ChatGPT-style)
- Runs completely offline using Ollama
- Clean and user-friendly Streamlit UI

---

## 🛠 Technology Stack

- **Python**
- **Streamlit** (Frontend UI)
- **Ollama** (Local LLM engine)
- **TinyLLaMA / LLaMA-based model**
- **Rule-based intent filtering**

---

## 🧠 How It Works

1. User enters a query in the chat interface
2. The system checks if the input is:
   - A greeting
   - A banking-related query
   - A non-banking query
3. Banking queries are forwarded to the Ollama LLM
4. Non-banking queries are politely rejected
5. Responses are displayed in the chat interface

---

## ▶️ How to Run the Project

### Step 1: Install dependencies
```bash
pip install -r requirements.txt


Step 2: Start Ollama

ollama run tinyllama

Step 3: Run the Streamlit app

streamlit run bankbot_app.py
