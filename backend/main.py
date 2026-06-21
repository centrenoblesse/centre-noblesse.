import os
import sqlite3
import smtplib
from datetime import datetime
from email.message import EmailMessage
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Configuration
ADMIN_EMAIL = "youcefkhadir091@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.environ.get("SMTP_EMAIL", "")  # Add your email here or set in ENV
SMTP_PASS = os.environ.get("SMTP_PASSWORD", "")  # Add your app password here or set in ENV
DB_NAME = "noblesse.db"

app = FastAPI(title="Centre Noblesse API")

# Allow CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with the domain name
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Initialization ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Registrations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email_address TEXT NOT NULL,
            selected_service TEXT NOT NULL,
            message TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            reason TEXT NOT NULL,
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Run DB init on startup
@app.on_event("startup")
def startup_event():
    init_db()

# --- Pydantic Models ---
class RegistrationRequest(BaseModel):
    name: str
    phone: str
    email: EmailStr
    course: str
    msg: Optional[str] = ""

class AppointmentRequest(BaseModel):
    name: str
    phone: str
    date: str
    reason: str

# --- Email Logic ---
def send_email_alert(subject: str, content: str):
    if not SMTP_USER or not SMTP_PASS:
        print("Warning: SMTP_EMAIL or SMTP_PASSWORD not configured. Email not sent.")
        print(f"Subject: {subject}\n{content}")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"Noblesse Website <{SMTP_USER}>"
    msg['To'] = ADMIN_EMAIL
    msg.set_content(content)

    try:
        # Using SSL
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- Endpoints ---
@app.post("/api/register")
async def register_student(req: RegistrationRequest, background_tasks: BackgroundTasks):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_registrations (student_name, phone_number, email_address, selected_service, message)
            VALUES (?, ?, ?, ?, ?)
        """, (req.name, req.phone, req.email, req.course, req.msg))
        conn.commit()
        conn.close()

        # Format email content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_body = f"""Nouvelle Inscription reçue !

Détails de l'étudiant :
----------------------
Nom complet : {req.name}
Téléphone : {req.phone}
Email : {req.email}

Formation sélectionnée :
------------------------
Cours/Pack : {req.course}

Message additionnel :
---------------------
{req.msg if req.msg else 'Aucun message'}

Enregistré le : {timestamp}
"""
        # Send email in background
        background_tasks.add_task(send_email_alert, f"[Inscription] {req.course} - {req.name}", email_body)
        
        return {"status": "success", "message": "Registration logged and email triggered."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/appointment")
async def request_appointment(req: AppointmentRequest, background_tasks: BackgroundTasks):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (name, phone_number, appointment_date, reason)
            VALUES (?, ?, ?, ?)
        """, (req.name, req.phone, req.date, req.reason))
        conn.commit()
        conn.close()

        # Format email content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_body = f"""Nouvelle demande de rendez-vous !

Détails du demandeur :
----------------------
Nom complet : {req.name}
Téléphone : {req.phone}

Détails du rendez-vous :
------------------------
Date souhaitée : {req.date}
Motif : {req.reason}

Enregistré le : {timestamp}
"""
        # Send email in background
        background_tasks.add_task(send_email_alert, f"[Rendez-vous] {req.name} le {req.date}", email_body)
        
        return {"status": "success", "message": "Appointment logged and email triggered."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running."}
