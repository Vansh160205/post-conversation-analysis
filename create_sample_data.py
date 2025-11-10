import requests
import time

BASE_URL = "http://localhost:8000/api"

conversations = [
    {
        "title": "Positive Support Experience",
        "messages": [
            {"sender": "user", "message": "Hi, I need help with my order"},
            {"sender": "ai", "message": "Sure! I'd be happy to help. What's your order number?"},
            {"sender": "user", "message": "It's #12345"},
            {"sender": "ai", "message": "Thank you! Your order has been shipped and will arrive tomorrow."},
            {"sender": "user", "message": "Perfect! Thanks so much for your help!"}
        ]
    },
    {
        "title": "Frustrated Customer",
        "messages": [
            {"sender": "user", "message": "This is the worst service ever! My order is late!"},
            {"sender": "ai", "message": "I sincerely apologize for the inconvenience. I understand your frustration. Let me look into this immediately."},
            {"sender": "user", "message": "You better fix this fast!"},
            {"sender": "ai", "message": "I've escalated this to our senior team. You'll receive a full refund and expedited shipping. Is there anything else I can help with?"},
            {"sender": "user", "message": "Fine. I hope this gets resolved."}
        ]
    },
    {
        "title": "Technical Issue",
        "messages": [
            {"sender": "user", "message": "My account login isn't working"},
            {"sender": "ai", "message": "I can help with that. Have you tried resetting your password?"},
            {"sender": "user", "message": "Yes, but I'm not receiving the reset email"},
            {"sender": "ai", "message": "Let me check your account settings. Can you confirm your email address?"},
            {"sender": "user", "message": "It's user@example.com"},
            {"sender": "ai", "message": "I found the issue. Your email was marked as spam. I've resent the reset link to your inbox."},
            {"sender": "user", "message": "Got it! Thanks, it's working now!"}
        ]
    },
    {
        "title": "AI Fallback Example",
        "messages": [
            {"sender": "user", "message": "What's the meaning of life?"},
            {"sender": "ai", "message": "I don't know the answer to that philosophical question. Is there something specific I can help you with?"},
            {"sender": "user", "message": "Can you predict lottery numbers?"},
            {"sender": "ai", "message": "I am unable to predict lottery numbers. I can help with customer support queries though."},
            {"sender": "user", "message": "Okay, never mind"}
        ]
    }
]

print("Creating sample conversations...\n")
for conv in conversations:
    response = requests.post(f"{BASE_URL}/conversations/", json=conv)
    if response.status_code == 201:
        conv_id = response.json()['id']
        print(f"✅ Created: {conv['title']} (ID: {conv_id})")
        
        # Trigger analysis
        analysis = requests.post(f"{BASE_URL}/analyse/", json={"conversation_id": conv_id})
        print(f"   Analysis queued: {analysis.json()['task_id']}\n")
        time.sleep(0.5)

print("\n🎉 Sample data created successfully!")
print("Run: curl http://localhost:8000/api/reports/ to see all analyses")