# ==========================================
# BankBot AI – Local LLM Banking Assistant
# Built using Streamlit + Ollama
# ==========================================

import streamlit as st
import uuid
from datetime import datetime
import requests

# ------------------------------------------
# Page Configuration
# ------------------------------------------
st.set_page_config(
    page_title="BankBot AI – Banking Assistant",
    layout="wide"
)

# ------------------------------------------
# Ollama Configuration
# ------------------------------------------
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "tinyllama"

# ------------------------------------------
# Session State Initialization
# ------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ------------------------------------------
# Utility Functions
# ------------------------------------------
def current_time():
    return datetime.now().strftime("%H:%M")

def is_greeting(message: str) -> bool:
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    return any(word in message.lower() for word in greetings)

def is_banking_related(message: str) -> bool:
    banking_terms = [
        "account", "loan", "emi", "interest",
        "card", "atm", "balance", "transaction",
        "ifsc", "branch", "bank"
    ]
    return any(term in message.lower() for term in banking_terms)

def generate_chat_title(messages):
    for msg in messages:
        if msg["role"] == "user":
            return msg["content"][:40]
    return "New Chat"

def reset_chat():
    st.session_state.current_chat = []
    st.session_state.chat_id = str(uuid.uuid4())
    st.session_state.user_input = ""

def save_chat():
    if not st.session_state.current_chat:
        return

    title = generate_chat_title(st.session_state.current_chat)
    st.session_state.chat_history.insert(0, {
        "id": st.session_state.chat_id,
        "title": title,
        "messages": st.session_state.current_chat.copy()
    })

# ------------------------------------------
# Ollama Response Handler
# ------------------------------------------
def get_ollama_response(user_question: str) -> str:
    """
    Sends the user query to Ollama and returns a clean banking response.
    """

    system_prompt = (
        "You are BankBot, a polite banking assistant.\n"
        "Answer only banking-related questions.\n"
        "Keep responses short and easy to read.\n"
        "Use bullet points when possible.\n"
        "Do not explain rules or instructions.\n"
    )

    full_prompt = f"""
{system_prompt}

Customer Question:
{user_question}

BankBot Answer:
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.3
        }
    }

    response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
    reply_text = response.json().get("response", "")

    # Safety cleanup
    blocked_phrases = ["You are BankBot", "Answer only", "Customer Question"]
    for phrase in blocked_phrases:
        reply_text = reply_text.replace(phrase, "")

    return reply_text.strip()

# ------------------------------------------
# Sidebar UI
# ------------------------------------------
with st.sidebar:
    st.markdown("## 🏦 BankBot AI")

    if st.button("➕ New Chat"):
        reset_chat()

    if st.button("💾 Save Chat"):
        save_chat()

    st.divider()
    st.markdown("### Chat History")

    for chat in st.session_state.chat_history:
        if st.button(chat["title"], key=chat["id"]):
            st.session_state.chat_id = chat["id"]
            st.session_state.current_chat = chat["messages"]

    st.divider()
    st.markdown("### Supported Topics")
    st.write("• Accounts")
    st.write("• Loans & EMI")
    st.write("• ATM & Cards")
    st.write("• Transactions")
    st.write("• Branch & IFSC")

# ------------------------------------------
# Main Interface
# ------------------------------------------
st.title("BankBot – AI Chatbot for Banking Queries")
st.caption("Local LLM powered • Privacy-friendly • Academic Project")
st.divider()

left_col, right_col = st.columns([3, 1])

# ------------------------------------------
# Chat Display
# ------------------------------------------
with left_col:
    for message in st.session_state.current_chat:
        alignment = "right" if message["role"] == "user" else "left"
        bg_color = "#0b5cff" if message["role"] == "user" else "#f1f3f5"
        text_color = "white" if message["role"] == "user" else "black"

        st.markdown(
            f"""
            <div style="text-align:{alignment};">
                <div style="
                    display:inline-block;
                    background:{bg_color};
                    color:{text_color};
                    padding:10px 14px;
                    border-radius:12px;
                    margin:6px;
                    max-width:80%;
                ">
                    <b>{message['role'].title()}</b> ({message['time']})<br>
                    {message['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ------------------------------------------
# Message Processing Logic
# ------------------------------------------
def send_message():
    user_text = st.session_state.user_input.strip()
    if not user_text:
        return

    # Store user message
    st.session_state.current_chat.append({
        "role": "user",
        "content": user_text,
        "time": current_time()
    })

    # Greeting handling
    if is_greeting(user_text):
        bot_reply = (
            "Hello 👋\n\n"
            "I’m **BankBot**, your banking assistant.\n\n"
            "You can ask me about:\n"
            "• Opening an account\n"
            "• Loans & EMI\n"
            "• Cards & ATM services"
        )

    # Non-banking query
    elif not is_banking_related(user_text):
        bot_reply = (
            "I’m here to help with **banking-related queries only**.\n\n"
            "Please ask about:\n"
            "• Accounts\n"
            "• Loans\n"
            "• Cards\n"
            "• ATM services"
        )

    # Valid banking query
    else:
        bot_reply = get_ollama_response(user_text)

    # Store bot reply
    st.session_state.current_chat.append({
        "role": "bot",
        "content": bot_reply,
        "time": current_time()
    })

    st.session_state.user_input = ""

# ------------------------------------------
# Input Section
# ------------------------------------------
st.divider()
st.text_input(
    "Ask a banking question...",
    key="user_input",
    placeholder="e.g. I want to open a savings account"
)
st.button("Send", on_click=send_message)

# ------------------------------------------
# Right Panel
# ------------------------------------------
with right_col:
    st.markdown("### Quick Actions")
    st.write("• Open Account")
    st.write("• Loan Information")
    st.write("• Card Services")
    st.write("• Branch Timings")

st.caption("Built for learning • Runs fully offline • MIT Licensed")
