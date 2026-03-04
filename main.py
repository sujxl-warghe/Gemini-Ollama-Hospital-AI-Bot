from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import requests, json, os

app = FastAPI()

# Serve frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")

# === Ollama model setup ===
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # better for hospital dialogues

# === Load hospital data ===
with open("data/hospital.json", "r", encoding="utf-8") as f:
    HOSPITAL_DATA = json.load(f)

# === Database Setup (SQLite) ===
DATABASE_URL = "sqlite:///data/appointments.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    date = Column(String)
    phone = Column(String)

Base.metadata.create_all(bind=engine)

# === Simple memory storage (per session) ===
chat_history = []

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")

# === New: Welcome message endpoint ===
@app.get("/welcome")
def welcome_message():
    """
    Returns a structured, formatted welcome message
    """
    return {
        "response": """
<p>Hello! 👋 Welcome to <strong>{name}</strong> in {location}. How can I assist you today?</p>
<p>You can ask about services, departments, doctors, or book an appointment.</p>
""".format(name=HOSPITAL_DATA["name"], location=HOSPITAL_DATA["location"])
    }

@app.post("/chat")
def chat_with_hospital_bot(user_query: str = Form(...)):
    """
    Main chatbot endpoint with short-term memory
    """
    global chat_history
    chat_history.append({"role": "user", "content": user_query})

    # Use only last 5 messages for memory
    context = "\n".join(
        [f"{m['role'].capitalize()}: {m['content']}" for m in chat_history[-5:]]
    )

    headers = {"Content-Type": "application/json"}
    prompt = f"""
You are a helpful, professional chatbot for {HOSPITAL_DATA['name']} in {HOSPITAL_DATA['location']}.
Use the following hospital info and chat history to answer accurately.

Hospital Information:
{json.dumps(HOSPITAL_DATA, indent=2)}

Chat History:
{context}

Guidelines:
- Be polite, clear, and empathetic.
- Format your answer with HTML tags: <p> for paragraphs, <ul><li> for lists, <strong> for bold text.
- Do NOT invent info not given in hospital data.
- If user wants to book an appointment, ask for their name, department, date, and phone number.
- Once user provides all info, confirm and tell them it's booked.

User: {user_query}
Chatbot:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "temperature": 0.3, "stream": False},
            headers=headers
        )

        response_data = response.text.strip()
        try:
            json_response = json.loads(response_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Invalid JSON response: {response_data}")

        bot_reply = json_response.get("response", "Sorry, I couldn't generate a reply.")
        chat_history.append({"role": "assistant", "content": bot_reply})

        return {"response": bot_reply}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/book")
def book_appointment(
    name: str = Form(...),
    department: str = Form(...),
    date: str = Form(...),
    phone: str = Form(...)
):
    """
    Endpoint to store appointment details
    """
    session = SessionLocal()
    new_appointment = Appointment(name=name, department=department, date=date, phone=phone)
    session.add(new_appointment)
    session.commit()
    session.close()
    return {"message": f"Appointment booked successfully for {name} on {date} with {department} department."}
