# 🤖 AI-Powered Debt Collection Agent

An AI-powered debt collection backend built using **FastAPI**, **Google Gemini AI**, and **SQLAlchemy** 
to automate customer interactions, recommend intelligent debt collection strategies, and streamline collection 
workflows through secure REST APIs.

## 🚀 Features

- 🔐 JWT Authentication & Role-Based Access Control
- 👥 Customer Management
- 📂 Collection Case Management
- 🤖 AI-Powered Customer Conversations (Google Gemini)
- 🧠 AI Collection Strategy Recommendation Engine
- 📜 Timeline & Activity Tracking
- 📊 Dashboard Analytics APIs
- ⚙️ Automated Collection Workflow
- 📄 Interactive Swagger API Documentation
  
## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic

### Authentication
- JWT Authentication
- OAuth2
- Passlib

### AI
- Google Gemini API
- Prompt Engineering

### Tools
- Git
- GitHub
- Postman
- Swagger UI

---

## 📁 Project Structure

```text
AI-Debt-Agent/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   └── main.py
│
├── data/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/inarendra15/AI-Debt-Agent.git
cd AI-Debt-Agent
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run the application

```bash
uvicorn app.main:app --reload
```

---

## 📖 API Documentation

After running the server:

**Swagger UI**

```
http://127.0.0.1:8000/docs
```

**ReDoc**

```
http://127.0.0.1:8000/redoc
```

---

## 🤖 AI Workflow

1. Customer interaction is received.
2. Google Gemini analyzes the conversation.
3. AI generates an appropriate response.
4. Collection strategy recommendation is generated.
5. Collection case workflow is updated.
6. Timeline events are recorded.
7. Dashboard analytics are updated.

---

## 🔒 Authentication

The application uses JWT-based authentication with role-based authorization.

Supported Roles:

- Admin
- Collection Agent

---

## 📌 Current Status

| Module | Status |
|---------|--------|
| Authentication | ✅ Completed |
| Customer Management | ✅ Completed |
| Collection Cases | ✅ Completed |
| AI Conversations | ✅ Completed |
| AI Recommendations | ✅ Completed |
| Timeline | ✅ Completed |
| Dashboard Analytics | ✅ Completed |
| Frontend (Next.js) | 🚧 In Progress |

---

## 🔮 Future Enhancements

- Next.js Frontend Dashboard
- PostgreSQL Support
- Docker Deployment
- Email & SMS Notifications
- Redis Caching
- Background Jobs
- Unit & Integration Tests
- CI/CD Pipeline

---

## 👨‍💻 Author

**Narendra Kumar**

GitHub: https://github.com/inarendra15

---

## ⭐ If you found this project useful, consider giving it a star!
