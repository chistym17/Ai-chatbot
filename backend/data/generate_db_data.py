import psycopg2
import uuid
from faker import Faker
from random import choice, randint, uniform
from datetime import datetime, timedelta

fake = Faker()

conn = psycopg2.connect(
    dbname="mydb",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cities = ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Seattle, WA", "Boston, MA"]
specializations = ["Cardiology", "Neurology", "Orthopedic Surgery", "General Practice", "Dermatology", "Oncology", "Pediatrics"]
diseases_list = [
    "Hypertension", "Diabetes", "Asthma", "Bronchitis", "Migraine", "Arthritis", "Lung Cancer", "Breast Cancer",
    "Depression", "Anxiety"] + [f"Disease {i}" for i in range(1, 91)]  
symptoms_list = ["cough", "fever", "fatigue", "pain", "headache", "nausea", "shortness of breath", "rash"]
treatments_list = ["Lisinopril", "Metformin", "Insulin", "Albuterol", "Ibuprofen", "Azithromycin", "Chemotherapy", "Surgery"]
medications_list = treatments_list + ["Atenolol", "Fluticasone", "Sumatriptan", "Paracetamol"]

cur.execute("SELECT id FROM hospitals")
hospitals = [row[0] for row in cur.fetchall()]  
for _ in range(50):
    hospital_id = str(uuid.uuid4())
    name = f"{fake.word().capitalize()} Hospital"
    location = choice(cities)
    contact = fake.unique.phone_number()[:12].replace(".", "-")
    established_date = fake.date_between(start_date="-50y", end_date="-5y")
    cur.execute(
        "INSERT INTO hospitals (id, name, location, contact, established_date) VALUES (%s, %s, %s, %s, %s)",
        (hospital_id, name, location, contact, established_date)
    )
    hospitals.append(hospital_id)

cur.execute("SELECT id FROM doctors")
doctors = [row[0] for row in cur.fetchall()]  
for _ in range(60):
    doctor_id = str(uuid.uuid4())
    hospital_id = choice(hospitals)
    name = f"Dr. {fake.first_name()} {fake.last_name()}"
    specialization = choice(specializations)
    years_of_experience = randint(1, 40)
    cur.execute(
        "INSERT INTO doctors (id, hospital_id, name, specialization, years_of_experience) VALUES (%s, %s, %s, %s, %s)",
        (doctor_id, hospital_id, name, specialization, years_of_experience)
    )
    doctors.append(doctor_id)

cur.execute("SELECT id, email FROM patients")
patients = [row[0] for row in cur.fetchall()]  
existing_emails = set(row[1] for row in cur.fetchall() if row[1] is not None)  

for _ in range(500):
    patient_id = str(uuid.uuid4())
    name = f"{fake.first_name()} {fake.last_name()}"
    age = randint(1, 100)
    gender = choice(["Male", "Female", "Other"])
    address = f"{randint(100, 999)} {fake.street_name()}, {choice(cities)}"
    phone = fake.unique.phone_number()[:12].replace(".", "-")
    
    email = f"{name.lower().replace(' ', '.')}@example.com"
    attempt = 1
    while email in existing_emails:
        email = f"{name.lower().replace(' ', '.')}{attempt}@example.com"
        attempt += 1
    existing_emails.add(email)
    
    created_at = fake.date_time_between(start_date="-5y", end_date="now")
    cur.execute(
        "INSERT INTO patients (id, name, age, gender, address, phone, email, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (patient_id, name, age, gender, address, phone, email, created_at)
    )
    patients.append(patient_id)

diseases = {}  
for disease_name in diseases_list:
    disease_id = str(uuid.uuid4())
    description = f"{disease_name} condition"
    symptoms = [choice(symptoms_list) for _ in range(randint(2, 5))]
    common_treatments = [choice(treatments_list) for _ in range(randint(1, 3))]
    created_at = fake.date_time_between(start_date="-5y", end_date="now")
    cur.execute(
        "INSERT INTO diseases (id, name, description, symptoms, common_treatments, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
        (disease_id, disease_name, description, symptoms, common_treatments, created_at)
    )
    diseases[disease_name] = disease_id

cur.execute("SELECT patient_id FROM medical_records")
medical_patients = [row[0] for row in cur.fetchall()]  
for _ in range(60):
    record_id = str(uuid.uuid4())
    patient_id = choice(patients)  
    diagnosis = choice(list(diseases.keys()))  
    medications = [choice(medications_list) for _ in range(randint(1, 3))]
    created_at = fake.date_time_between(start_date="-5y", end_date="now")
    doctor_id = choice(doctors)
    cur.execute(
        "INSERT INTO medical_records (id, patient_id, diagnosis, medications, created_at, doctor_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (record_id, patient_id, diagnosis, medications, created_at, doctor_id)
    )
    medical_patients.append(patient_id)

for _ in range(60):
    appt_id = str(uuid.uuid4())
    doctor_id = choice(doctors)
    patient_id = choice(medical_patients)  
    appointment_date = fake.date_time_between(start_date="now", end_date="+1y")
    status = choice(["scheduled"] * 8 + ["completed"] * 2 + ["canceled"] * 1)
    cur.execute(
        "INSERT INTO appointments (id, doctor_id, patient_id, appointment_date, status) VALUES (%s, %s, %s, %s, %s)",
        (appt_id, doctor_id, patient_id, appointment_date, status)
    )

conn.commit()
print("Bulk data inserted successfully with diseases linked to appointments via medical_records!")

cur.close()
conn.close()