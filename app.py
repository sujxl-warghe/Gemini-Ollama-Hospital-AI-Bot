from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from google import genai
from dotenv import load_dotenv
import os, json

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set")

client = genai.Client(api_key=API_KEY)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")


# -------- Hospital Data --------
with open("data/hospital.json", "r", encoding="utf-8") as f:
    HOSPITAL_DATA = json.load(f)


# -------- Database Setup --------
DATABASE_URL = "sqlite:///data/appointments.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department = Column(String)
    date = Column(String)
    phone = Column(String)


Base.metadata.create_all(bind=engine)


chat_history = []


@app.get("/welcome")
def welcome():
    return {
        "response": f"""
<p>Hello! 👋 Welcome to <strong>{HOSPITAL_DATA['name']}</strong> in {HOSPITAL_DATA['location']}.
How can I assist you today?</p>
"""
    }


@app.post("/chat")
def chat(user_query: str = Form(...)):
    global chat_history

    chat_history.append({"role": "user", "content": user_query})

    history = "\n".join(
        [f"{m['role'].capitalize()}: {m['content']}" for m in chat_history[-5:]]
    )

    prompt = f"""
You are a polite, helpful hospital chatbot.

Hospital Info:
{json.dumps(HOSPITAL_DATA, indent=2)}

Chat History:
{history}

Rules:
- Answer in simple English using HTML tags (<p>, <strong>, <ul><li>)
- Do NOT make up data
- If user wants appointment ask: Name, Department, Date, Phone
- When all info given — confirm.

User: {user_query}
"""

    result = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    reply = result.text.strip()

    chat_history.append({"role": "assistant", "content": reply})

    return {"response": reply}


@app.post("/book")
def book(name: str = Form(...), department: str = Form(...),
         date: str = Form(...), phone: str = Form(...)):

    session = SessionLocal()
    new = Appointment(name=name, department=department, date=date, phone=phone)
    session.add(new)
    session.commit()
    session.close()

    return {"message": f"Appointment booked for {name} on {date} in {department}."}
