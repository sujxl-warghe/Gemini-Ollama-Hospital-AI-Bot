# 🏥 Health is Heaven — AI Hospital Chatbot

An AI-powered hospital chatbot built using **FastAPI**, **Gemini-2.5-Flash**, and **Ollama (Mistral)**.
It answers hospital-related queries and supports **appointment booking stored in a SQLite database**, all through a clean chat interface.

---

# ✨ Features

* 🤖 AI chatbot powered by **Gemini-2.5-Flash**
* 🧠 Optional **local LLM support with Ollama (Mistral)**
* 🏥 Hospital knowledge loaded from JSON
* 📅 Appointment booking stored in SQLite database
* 💬 Context-aware chat (short conversation memory)
* 🎨 Clean chat UI (HTML, CSS, JavaScript)
* 🔐 Secure API key management using `.env`
* ⚡ FastAPI backend for high performance

---

# 🧠 Models Used

| File    | Model            | Type     |
| ------- | ---------------- | -------- |
| app.py  | Gemini-2.5-Flash | Cloud AI |
| main.py | Mistral (Ollama) | Local AI |

You can run **either model or both depending on your requirement.**

---

# 📂 Project Structure

Hospital/
Hospital-AI-Chatbot/
│
├── app.py                 # FastAPI server using Gemini-2.5-Flash
├── main.py                # FastAPI server using Ollama (Mistral)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .env                   # Environment variables (ignored in git)
│
├── data/
│   ├── hospital.json      # Hospital information dataset
│   └── appointments.db    # SQLite database (auto-generated)
│
└── static/
    ├── index.html         # Chatbot user interface
    ├── style.css          # UI styling
    └── script.js          # Frontend chat logic

---

# 🔐 Environment Setup

Create a `.env` file in the root folder:

GOOGLE_API_KEY=your_real_key_here


---

# 📦 Install Dependencies

pip install -r requirements.txt

or install manually:

pip install fastapi uvicorn sqlalchemy python-dotenv google-genai requests

---

# 🚀 Run Gemini Chatbot (Cloud AI)

uvicorn app:app --reload

Open in browser:

http://127.0.0.1:8000

---

# 💻 Run Local Mistral Chatbot (Ollama)

Step 1 — Install Ollama
https://ollama.ai

Step 2 — Download Mistral model

ollama pull mistral

Step 3 — Run the API

uvicorn main:app --reload

---

# 🗄 Database

All appointment bookings are stored in:

data/appointments.db

Database technology: **SQLite with SQLAlchemy ORM**

---

# 📑 API Endpoints

Load UI

GET /

Welcome message

GET /welcome

Chat with bot

POST /chat

Form-Data

user_query : text

Book appointment

POST /book

Form-Data

name : string
department : string
date : string
phone : string

---

# 🎨 UI Highlights

* Dark modern chat interface
* Chat bubbles
* User and bot message alignment
* Responsive layout
* Clean minimal design

---

# 🧪 Tech Stack

Python
FastAPI
Gemini-2.5-Flash
Ollama (Mistral)
SQLite + SQLAlchemy
HTML
CSS
JavaScript
python-dotenv

---

# 🔒 Security

* Never expose API keys
* Use `.gitignore` for `.env` and `venv`
* Rotate keys if they are leaked

---

# 💡 Future Improvements

* Doctor & department listing
* Admin dashboard
* Chat history database
* Voice assistant support
* Authentication system
* Email / SMS appointment reminders

---

# 👨‍💻 Author

Sujal Warghe

---

# ⭐ Support

If you like this project, please give it a **star ⭐ on GitHub**.
