import requests
import json

BASE_URL = "http://localhost:8000/api"

# Test 1: Upload conversation
print("Test 1: Uploading conversation...")
response = requests.post(f"{BASE_URL}/conversations/", json={
    "title": "API Test Chat",
    "messages": [
        {"sender": "user", "message": "Hello, I need help"},
        {"sender": "ai", "message": "Sure! How can I assist you?"},
        {"sender": "user", "message": "Thanks, you're helpful!"}
    ]
})
print(f"Status: {response.status_code}")
conversation_id = response.json()['id']
print(f"Created Conversation ID: {conversation_id}\n")

# Test 2: Trigger analysis
print("Test 2: Triggering analysis...")
response = requests.post(f"{BASE_URL}/analyse/", json={
    "conversation_id": conversation_id
})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test 3: Get all reports
print("Test 3: Fetching all reports...")
response = requests.get(f"{BASE_URL}/reports/")
print(f"Status: {response.status_code}")
print(f"Total Reports: {len(response.json())}\n")

# Test 4: Get specific analysis
print(f"Test 4: Fetching analysis for conversation {conversation_id}...")
import time
time.sleep(1)  # Wait for async processing
response = requests.get(f"{BASE_URL}/reports/")
for report in response.json():
    if report['conversation_id'] == conversation_id:
        print(json.dumps(report, indent=2))