import json
import requests

# Hasura endpoint (adjust if different)
HASURA_URL = "http://localhost:8080/v1/graphql"
# Hasura admin secret (if required, uncomment and set)
# HASURA_ADMIN_SECRET = "your-admin-secret-here"
HEADERS = {
    "Content-Type": "application/json",
    # "x-hasura-admin-secret": HASURA_ADMIN_SECRET  # Uncomment if needed
}

# Input and output files
INPUT_FILE = "training_data.jsonl"
WORKING_FILE = "working_data.jsonl"
ERROR_FILE = "error_data.jsonl"

import requests

def test_query(query):
    """Send a query to Hasura and return True if data exists, False otherwise."""
    payload = {"query": query}
    try:
        response = requests.post(HASURA_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Raise exception for HTTP errors
        result = response.json()
        
        if "errors" in result:
            return False, result["errors"]  # Query failed due to errors

        if "data" in result:
            data = result["data"]
            # Check if any key in "data" contains a non-empty list/dict
            if any(data[key] for key in data):
                return True, None  # Data exists
            else:
                return False, "Query executed successfully but returned empty data."

        return False, "Unknown response structure."

    except requests.RequestException as e:
        return False, str(e)


def process_training_data():
    working_data = []
    error_data = []
    
    # Read training data
    with open(INPUT_FILE, "r") as f:
        for line in f:
            item = json.loads(line.strip())
            prompt = item["prompt"]
            query = item["query"]
            
            # Test the query
            success, error = test_query(query)
            if success:
                working_data.append({"prompt": prompt, "query": query})
                print(f"✓ Success: {prompt}")
            else:
                error_data.append({"prompt": prompt, "query": query, "error": error})
                print(f"✗ Error: {prompt} - {error}")
    
    # Save working data
    with open(WORKING_FILE, "w") as f:
        for item in working_data:
            f.write(json.dumps(item) + "\n")
    print(f"Saved {len(working_data)} working queries to {WORKING_FILE}")
    
    # Save error data
    with open(ERROR_FILE, "w") as f:
        for item in error_data:
            f.write(json.dumps(item) + "\n")
    print(f"Saved {len(error_data)} error queries to {ERROR_FILE}")

if __name__ == "__main__":
    print("Starting query validation...")
    process_training_data()