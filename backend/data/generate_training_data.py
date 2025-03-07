import psycopg2
import json
from random import choice, randint
from datetime import datetime

# Database connection (replace with your details)
conn = psycopg2.connect(
    dbname="mydb",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Fetch real data from the database
cur.execute("SELECT name FROM diseases")
diseases = [row[0] for row in cur.fetchall()]

cur.execute("SELECT specialization FROM doctors")
specializations = list(set(row[0] for row in cur.fetchall()))

cur.execute("SELECT location FROM hospitals")
locations = list(set(row[0] for row in cur.fetchall()))

cur.execute("SELECT DISTINCT status FROM appointments")
statuses = [row[0] for row in cur.fetchall()]

# Sample years and age thresholds
years = [2020, 2021, 2022, 2023, 2024, 2025]
ages = [18, 30, 50, 65]
genders = ["Male", "Female", "Other"]

# Number of datapoints (adjustable)
NUM_EXAMPLES = 500  # Change to 100, 1000, etc. as needed

# Generate training data
dataset = []
for _ in range(NUM_EXAMPLES):
    query_type = randint(1, 6)

    if query_type == 1:  # Patients by diagnosis and date
        diagnosis = choice(diseases)
        year = choice(years)
        prompt = f"Patients with {diagnosis} diagnosed after {year}"
        completion = (
            f"query {{ medical_records(where: {{ diagnosis: {{ _eq: \"{diagnosis}\" }}, "
            f"created_at: {{ _gt: \"{year}-01-01\" }} }}) {{ id patient {{ id name age gender }} "
            f"diagnosis created_at }} }}"
        )

    elif query_type == 2:  # Patients by age and gender
        gender = choice(genders)
        age_limit = choice(ages)
        prompt = f"{gender} patients {'under' if age_limit <= 30 else 'over'} {age_limit} years old"
        completion = (
            f"query {{ patients(where: {{ gender: {{ _eq: \"{gender}\" }}, "
            f"age: {{ {'_lt' if age_limit <= 30 else '_gt'}: {age_limit} }} }}) "
            f"{{ id name age gender created_at }} }}"
        )

    elif query_type == 3:  # Appointments by status and date
        status = choice(statuses)
        year = choice(years)
        prompt = f"Appointments {status} after {year}"
        completion = (
            f"query {{ appointments(where: {{ status: {{ _eq: \"{status}\" }}, "
            f"appointment_date: {{ _gt: \"{year}-01-01\" }} }}) {{ id patient {{ name }} "
            f"doctor {{ name }} appointment_date status }} }}"
        )

    elif query_type == 4:  # Patients by doctor specialization
        specialization = choice(specializations)
        prompt = f"Patients treated by {specialization} specialists"
        completion = (
            f"query {{ medical_records(where: {{ doctor: {{ specialization: {{ _eq: \"{specialization}\" }} }} }}) "
            f"{{ id patient {{ id name age }} diagnosis doctor {{ name specialization }} }} }}"
        )

    elif query_type == 5:  # Patients by diagnosis and hospital location
        diagnosis = choice(diseases)
        location = choice(locations)
        prompt = f"Patients with {diagnosis} treated in {location} hospitals"
        completion = (
            f"query {{ medical_records(where: {{ diagnosis: {{ _eq: \"{diagnosis}\" }}, "
            f"doctor: {{ hospital: {{ location: {{ _eq: \"{location}\" }} }} }} }}) "
            f"{{ id patient {{ name }} diagnosis doctor {{ hospital {{ name location }} }} }} }}"
        )

    elif query_type == 6:  # Patients with appointments and diagnosis
        diagnosis = choice(diseases)
        year = choice(years)
        prompt = f"Patients with {diagnosis} who had appointments after {year}"
        completion = (
            f"query {{ appointments(where: {{ patient: {{ medical_records: {{ diagnosis: {{ _eq: \"{diagnosis}\" }} }} }}, "
            f"appointment_date: {{ _gt: \"{year}-01-01\" }} }}) {{ id patient {{ name }} "
            f"appointment_date doctor {{ name }} }} }}"
        )

    dataset.append({"prompt": prompt, "completion": completion})

# Save to JSONL
with open("training_data.jsonl", "w") as f:
    for entry in dataset:
        f.write(json.dumps(entry) + "\n")

print(f"Generated {NUM_EXAMPLES} training datapoints in training_data.jsonl!")

# Close the connection
cur.close()
conn.close()