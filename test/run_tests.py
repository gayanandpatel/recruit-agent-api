import json
import requests
import time

# Load your test cases
with open('test_cases.json', 'r') as f:
    test_cases = json.load(f)

url = "http://127.0.0.1:8000/api/v1/evaluate"

for i, case in enumerate(test_cases, 1):
    print(f"\n--- Running Test {i} ---")
    candidate_name = case['resume_text'].split('\n')[0]
    print(f"Candidate: {candidate_name}")
    
    response = requests.post(url, json=case)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Score: {result['final_score']}")
        print(f"Summary: {result['evaluation_summary']}")
        print(f"Missing: {result['missing_skills']}")
    else:
        print(f"Error: {response.text}")
        
    time.sleep(1) # Give the API provider a second to breathes