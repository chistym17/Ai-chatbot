from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from fastapi.middleware.cors import CORSMiddleware
from db.model import Patient, Doctor, Hospital, Disease, Appointment, MedicalRecord
import dotenv

import os

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/patients")
async def get_patients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient.id, Patient.name, Patient.age, Patient.gender, Patient.phone, Patient.email))
    return result.mappings().all()

@app.get("/doctors")
async def get_doctors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor.id, Doctor.name, Doctor.specialization, Doctor.years_of_experience, Doctor.hospital_id))
    return result.mappings().all()

@app.get("/hospitals")
async def get_hospitals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hospital.id, Hospital.name, Hospital.location, Hospital.contact, Hospital.established_date))
    return result.mappings().all()

@app.get("/diseases")
async def get_diseases(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Disease.id, Disease.name, Disease.description, Disease.symptoms, Disease.common_treatments))
    return result.mappings().all()

@app.get("/appointments")
async def get_appointments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment.id, Appointment.doctor_id, Appointment.patient_id, Appointment.appointment_date, Appointment.status))
    return result.mappings().all()

@app.get("/medical_records")
async def get_medical_records(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MedicalRecord.id, MedicalRecord.patient_id, MedicalRecord.diagnosis, MedicalRecord.medications, MedicalRecord.created_at, MedicalRecord.doctor_id))
    return result.mappings().all()
