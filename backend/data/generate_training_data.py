import json
import random
from datetime import datetime, timedelta
import re

names = ["Alice Smith", "John Doe", "Michael Brown", "Sarah Johnson", "David Wilson", "Emma Davis", "James Taylor", "Olivia Lee"]
diseases = ["diabetes", "hypertension", "asthma", "cancer", "flu", "pneumonia", "migraine", "arthritis"]
specializations = ["Cardiology", "Neurology", "Pediatrics", "Orthopedics", "Oncology", "Endocrinology", "Pulmonology"]
locations = ["New York", "California", "Texas", "Florida", "Illinois", "Ohio"]
statuses = ["scheduled", "completed", "cancelled"]

def random_date(start_year=2015, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%dT00:00:00Z")

def format_query(query_template, values):
    formatted_query = query_template.format(**values)
    
    formatted_query = re.sub(r'\\"', '"', formatted_query)
    
    return formatted_query

query_templates = [
    (
        "Find all patients diagnosed with {disease} and their doctors.",
        'query {{ medical_records(where: {{ diagnosis: {{ _ilike: "%{disease}%" }} }}) {{ id diagnosis patient {{ id name age }} doctor {{ id name specialization }} }} }}'
    ),
    (
        "List all doctors with more than {years} years of experience and their hospitals.",
        "query {{ doctors(where: {{ years_of_experience: {{ _gt: {years} }} }}) {{ id name specialization hospital {{ id name location }} }} }}"
    ),
    (
        "Get all upcoming appointments for a patient named {name}.",
        'query {{ appointments(where: {{ patient: {{ name: {{ _eq: "{name}" }} }}, appointment_date: {{ _gt: "2025-03-09T00:00:00Z" }} }}) {{ id appointment_date doctor {{ id name specialization }} }} }}'
    ),
    (
        "Find all hospitals along with their doctors and total patients treated by each doctor.",
        "query {{ hospitals {{ id name location doctors {{ id name specialization medical_records_aggregate {{ aggregate {{ count }} }} }} }} }}"
    ),
    (
        "Retrieve details of a patient named {name} including their medical history and doctors.",
        'query {{ patients(where: {{ name: {{ _eq: "{name}" }} }}) {{ id name age medical_records {{ id diagnosis medications doctor {{ id name specialization }} }} }} }}'
    ),
    (
        "List the top {limit} doctors with the most medical records.",
        "query {{ doctors(order_by: [{{ medical_records_aggregate: {{ count: desc }} }}], limit: {limit}) {{ id name specialization }} }}"
    ),
    (
        "List hospitals in {location} with doctors specializing in {specialization}.",
        'query {{ hospitals(where: {{ location: {{ _eq: "{location}" }} }}) {{ id name location doctors(where: {{ specialization: {{ _eq: "{specialization}" }} }}) {{ id name specialization }} }} }}'
    ),
    (
        "Find all appointments scheduled after {date} with status {status}.",
        'query {{ appointments(where: {{ appointment_date: {{ _gt: "{date}" }}, status: {{ _eq: "{status}" }} }}) {{ id appointment_date patient {{ name }} doctor {{ name specialization }} status }} }}'
    ),
    (
        "Get all diseases with symptoms including {symptom}.",
        'query {{ diseases(where: {{ symptoms: {{ _contains: ["{symptom}" ] }} }}) {{ id name description symptoms common_treatments }} }}'
    ),
    (
        "Find patients over {age} years old diagnosed with {disease}.",
        'query {{ patients(where: {{ age: {{ _gt: {age} }}, medical_records: {{ diagnosis: {{ _ilike: "%{disease}%" }} }} }}) {{ id name age medical_records {{ diagnosis }} }} }}'
    ),
    (
        "List doctors in {location} with less than {years} years of experience.",
        'query {{ doctors(where: {{ hospital: {{ location: {{ _eq: "{location}" }} }}, years_of_experience: {{ _lt: {years} }} }}) {{ id name specialization hospital {{ name location }} }} }}'
    ),
    (
        "Find the total number of appointments per hospital in {location}.",
        'query {{ hospitals(where: {{ location: {{ _eq: "{location}" }} }}) {{ id name location doctors {{ medical_records_aggregate {{ aggregate {{ count }} }} }} }} }}'
    ),
    (
        "Get medical records created after {date} for patients with {disease}.",
        'query {{ medical_records(where: {{ created_at: {{ _gt: "{date}" }}, diagnosis: {{ _ilike: "%{disease}%" }} }}) {{ id diagnosis patient {{ name age }} doctor {{ name }} }} }}'
    ),
    (
        "List patients with appointments scheduled with doctors specializing in {specialization}.",
        'query {{ appointments(where: {{ doctor: {{ specialization: {{ _eq: "{specialization}" }} }} }}) {{ id patient {{ id name age }} doctor {{ name specialization }} appointment_date }} }}'
    ),
    (
        "Find all doctors who treated patients with {disease} in the past year.",
        'query {{ medical_records(where: {{ diagnosis: {{ _ilike: "%{disease}%" }}, created_at: {{ _gt: "2024-01-01T00:00:00Z" }} }}) {{ doctor {{ id name specialization hospital {{ name }} }} }} }}'
    ),
    (
        "List all hospitals in {location} that have more than {count} doctors.",
        'query {{ hospitals(where: {{ location: {{ _eq: "{location}" }}, doctors_aggregate: {{ count: {{ _gt: {count} }} }} }}) {{ id name location doctors_aggregate {{ count }} }} }}'
    ),
    (
        "Get the number of patients treated by each doctor specializing in {specialization}.",
        'query {{ doctors(where: {{ specialization: {{ _eq: "{specialization}" }} }}) {{ id name medical_records_aggregate {{ count }} hospital {{ name }} }} }}'
    ),
    (
        "Find patients who had appointments with multiple doctors in {specialization}.",
        'query {{ patients(where: {{ appointments: {{ doctor: {{ specialization: {{ _eq: "{specialization}" }} }} }} }}) {{ id name appointments {{ doctor {{ name specialization }} }} }} }}'
    ),
    (
        "List all medical records created between {date} and today for {disease}.",
        'query {{ medical_records(where: {{ created_at: {{ _gt: "{date}" }}, diagnosis: {{ _ilike: "%{disease}%" }} }}) {{ id diagnosis patient {{ name }} doctor {{ name }} created_at }} }}'
    ),
    (
        "Find hospitals that have doctors with experience greater than {years} years in {specialization}.",
        'query {{ hospitals {{ id name doctors(where: {{ years_of_experience: {{ _gt: {years} }}, specialization: {{ _eq: "{specialization}" }} }}) {{ name years_of_experience }} }} }}'
    ),
    (
        "Get all appointments scheduled for next week with doctors specializing in {specialization}.",
        'query {{ appointments(where: {{ appointment_date: {{ _gt: "2024-03-11T00:00:00Z", _lt: "2024-03-18T00:00:00Z" }}, doctor: {{ specialization: {{ _eq: "{specialization}" }} }} }}) {{ id appointment_date patient {{ name }} doctor {{ name }} }} }}'
    ),
    (
        "List patients who have been diagnosed with both {disease} and had appointments in {location} hospitals.",
        'query {{ patients(where: {{ medical_records: {{ diagnosis: {{ _ilike: "%{disease}%" }} }}, appointments: {{ doctor: {{ hospital: {{ location: {{ _eq: "{location}" }} }} }} }} }}) {{ id name medical_records {{ diagnosis }} }} }}'
    ),
    (
        "Find doctors who have treated more than {count} patients with {disease}.",
        'query {{ doctors(where: {{ medical_records: {{ diagnosis: {{ _ilike: "%{disease}%" }} }} }}, order_by: {{ medical_records_aggregate: {{ count: desc }} }}) {{ id name specialization medical_records_aggregate {{ count }} }} }}'
    ),
    (
        "Get all medical records where the patient age is above {age} and treated by doctors with more than {years} years experience.",
        "query {{ medical_records(where: {{ patient: {{ age: {{ _gt: {age} }} }}, doctor: {{ years_of_experience: {{ _gt: {years} }} }} }}) {{ diagnosis patient {{ name age }} doctor {{ name years_of_experience }} }} }}"
    )
]

class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        result = super().encode(obj)
        return result.replace('\\\\"', '\\"','\'','/')

def generate_training_data(num_samples=500):
    training_data = []
    
    for _ in range(num_samples):
        template = random.choice(query_templates)
        
        name = random.choice(names)
        disease = random.choice(diseases)
        years = random.randint(1, 30)
        count = random.randint(1, 20)
        limit = random.randint(1, 10)
        location = random.choice(locations)
        specialization = random.choice(specializations)
        date = random_date()
        symptom = random.choice(["fever", "cough", "pain", "fatigue"])
        age = random.randint(18, 90)
        status = random.choice(statuses)
        
        values = {
            "name": name,
            "disease": disease,
            "years": years,
            "count": count,
            "limit": limit,
            "location": location,
            "specialization": specialization,
            "date": date,
            "symptom": symptom,
            "age": age,
            "status": status
        }
        
        prompt = template[0].format(**values)
        
        query_template = template[1]
        formatted_query = query_template.format(**values)
        
        training_data.append({"prompt": prompt, "query": formatted_query})
    
    with open("training_data.jsonl", "w") as f:
        for item in training_data:
            prompt_json = json.dumps(item["prompt"])
            query_str = item["query"]
            query_json = json.dumps(query_str)
            
            f.write(f'{{"prompt": {prompt_json}, "query": {query_json}}}' + "\n")
    
    print(f"Generated {num_samples} training samples in training_data.jsonl")

generate_training_data(5000)