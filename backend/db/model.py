from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey, TIMESTAMP, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hospital_id = Column(UUID(as_uuid=True), ForeignKey("hospitals.id"), nullable=False)
    name = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=False)
    years_of_experience = Column(Integer, nullable=False)

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    location = Column(Text, nullable=False)
    contact = Column(String(20), nullable=False)
    established_date = Column(Date, nullable=False)

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    symptoms = Column(ARRAY(Text), nullable=True)
    common_treatments = Column(ARRAY(Text), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    appointment_date = Column(TIMESTAMP, nullable=False)
    status = Column(String(50), nullable=False)

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    diagnosis = Column(Text, nullable=False)
    medications = Column(ARRAY(Text), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False)
