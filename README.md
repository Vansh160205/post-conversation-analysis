# 🤖 Post-Conversation Analysis System

Django REST Framework application for automated AI conversation analysis with real-time processing and daily batch jobs.

---

## 📋 Features

- ✅ **11 Analysis Parameters**: Clarity, Relevance, Accuracy, Completeness, Sentiment, Empathy, Response Time, Resolution Rate, Escalation Detection, Fallback Frequency, Overall Score
- ✅ **REST API**: Upload conversations, trigger analysis, fetch reports
- ✅ **Async Processing**: Celery-based background tasks
- ✅ **Daily Auto-Analysis**: Scheduled batch processing at midnight
- ✅ **PostgreSQL Database**: Production-ready data storage

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7 + Django REST Framework 3.14.0
- **Database**: PostgreSQL (or SQLite for dev)
- **Task Queue**: Celery 5.3.4 + Redis 4.5.5
- **Scheduler**: Celery Beat (django-celery-beat 2.5.0)

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd post-conversation-analysis
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
# For PostgreSQL (recommended)
createdb conversation_analysis

# Update settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'conversation_analysis',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start Redis (for Celery)
```bash
# Install Redis first: https://redis.io/download
redis-server
```

---

## 🚀 Running the Application

### Terminal 1: Django Server
```bash
python manage.py runserver
```

### Terminal 2: Celery Worker
```bash
celery -A post_conversation_analysis worker --loglevel=info
```

### Terminal 3: Celery Beat (Scheduler)
```bash
celery -A post_conversation_analysis beat --loglevel=info
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### 1. Upload Conversation
**Endpoint**: `POST /api/conversations/`

**Request Body**:
```json
{
  "title": "Customer Support Chat",
  "messages": [
    {"sender": "user", "message": "Hi, I need help with my order."},
    {"sender": "ai", "message": "Sure! Can you share your order ID?"},
    {"sender": "user", "message": "It's 12345."},
    {"sender": "ai", "message": "Thanks! Your order has been shipped."}
  ]
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "title": "Customer Support Chat",
  "created_at": "2025-11-09T12:00:00Z"
}
```

---

### 2. Trigger Analysis
**Endpoint**: `POST /api/analyse/`

**Request Body**:
```json
{
  "conversation_id": 1
}
```

**Response** (202 Accepted):
```json
{
  "message": "Analysis queued",
  "task_id": "abc123-def456",
  "conversation_id": 1
}
```

---

### 3. Get Analysis Reports
**Endpoint**: `GET /api/reports/`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "conversation_id": 1,
    "clarity_score": 4.5,
    "relevance_score": 4.8,
    "accuracy_score": 4.7,
    "completeness_score": 4.2,
    "sentiment": "positive",
    "empathy_score": 0.0,
    "response_time_avg": 12.5,
    "resolution_rate": true,
    "escalation_need": false,
    "fallback_frequency": 0,
    "overall_score": 4.55,
    "created_at": "2025-11-09T12:05:00Z"
  }
]
```

---

## ⏰ Cron Job Setup

### Automatic (via Celery Beat)
Celery Beat automatically runs `run_daily_analysis` task every day at midnight.

**Configured in `settings.py`**:
```python
CELERY_BEAT_SCHEDULE = {
    'daily-conversation-analysis': {
        'task': 'analysis.tasks.run_daily_analysis',
        'schedule': crontab(hour=0, minute=0),
    },
}
```

### Manual Trigger
```bash
python manage.py run_daily_analysis
```

---

## 🧪 Testing

### Test API with cURL

**1. Upload Conversation**:
```bash
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Chat",
    "messages": [
      {"sender": "user", "message": "Hello"},
      {"sender": "ai", "message": "Hi! How can I help?"}
    ]
  }'
```

**2. Trigger Analysis**:
```bash
curl -X POST http://localhost:8000/api/analyse/ \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 1}'
```

**3. Get Reports**:
```bash
curl http://localhost:8000/api/reports/
```

---

## 📊 Analysis Parameters

| Category | Parameter | Description |
|----------|-----------|-------------|
| **Quality** | Clarity | Message clarity (1-5) |
| | Relevance | Topic consistency (1-5) |
| | Accuracy | Factual correctness (1-5) |
| | Completeness | Answer depth (1-5) |
| **Interaction** | Sentiment | positive/neutral/negative |
| | Empathy | Empathy shown (1-5, negative only) |
| | Response Time | Avg seconds between messages |
| **Resolution** | Resolution Rate | Issue resolved (true/false) |
| | Escalation Need | Human escalation needed (true/false) |
| **AI Ops** | Fallback Frequency | Count of "I don't know" |
| **Overall** | Overall Score | Weighted average (1-5) |

---

## 🏗️ Project Structure

```
post-conversation-analysis/
├── analysis/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── run_daily_analysis.py
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API endpoints
│   ├── analyzer.py        # Analysis logic
│   ├── tasks.py           # Celery tasks
│   └── urls.py
├── post_conversation_analysis/
│   ├── settings.py
│   ├── celery.py          # Celery config
│   └── urls.py
├── requirements.txt
└── README.md
```

---

## 🐛 Troubleshooting

### Issue: Celery not connecting to Redis
**Solution**: Ensure Redis is running on port 6379
```bash
redis-cli ping  # Should return "PONG"
```

### Issue: Database connection errors
**Solution**: Check PostgreSQL service and credentials in settings.py

### Issue: ImportError for celery
**Solution**: Ensure `__init__.py` in project root imports celery app

---

## 📝 Future Enhancements

- [ ] Real-time WebSocket notifications
- [ ] Multi-language sentiment analysis
- [ ] Integration with Claude API for advanced analysis
- [ ] Dashboard UI with charts
- [ ] Export reports to PDF/CSV

---

## 🎥 Demo Video

**Loom Video**: [Add your Loom video link here]

Quick walkthrough covering:
- Project architecture
- Code explanation
- API testing (Postman)
- Celery async processing
- Daily cron job demo
- Database inspection

---

## 👨‍💻 Developer

**Kipps.AI Internship Assignment**  
Submitted by: Vansh Vagadia  
Contact: vanshvagadia1602@gmail.com
GitHub: Vansh160205
---

## 🙏 Acknowledgments

- Django & DRF documentation
- Celery documentation
- Kipps.AI team for the opportunity

---

## 📄 License

MIT License