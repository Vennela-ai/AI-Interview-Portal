# 🤖 AI Interview Portal

An AI-powered interview preparation platform built with **Flask** and **Google Gemini AI** that helps students and job seekers practice technical and HR interviews with instant AI-generated feedback.

---

## 🚀 Features

###  User Authentication
- User Registration
- Secure Login
- Password Hashing
- Session Management
- Change Password

###  AI Interview
- Generate AI-based interview questions
- Select:
  - Job Role
  - Experience Level
  - Skills
  - Interview Type
  - Difficulty Level
- One Question at a Time Interface
- Progress Bar
- Countdown Timer
- Auto-save Answers
- Character Counter

### 🤖 AI Evaluation
- AI evaluates answers using Google Gemini
- Overall Interview Score
- Detailed Feedback
- Performance Analysis

###  Dashboard
- Total Interviews
- Average Score
- Best Score
- Recent Interview History

### Reports
- Download Interview Report as PDF
- View Previous Interviews

---

# 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Flask (Python)

### Database
- SQLite
- SQLAlchemy ORM

### AI
- Google Gemini API

### Authentication
- Werkzeug Security

### PDF Generation
- ReportLab

### Version Control
- Git
- GitHub

---

# 📂 Project Structure

```
AI-Interview-Portal
│
├── static
│   ├── css
│   ├── js
│   └── images
│
├── templates
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── interview.html
│   ├── result.html
│   ├── history.html
│   └── profile.html
│
├── app.py
├── models.py
├── gemini_service.py
├── pdf_generator.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Vennela-ai/AI-Interview-Portal.git
```

Go to the project folder

```bash
cd AI-Interview-Portal
```

Create a virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the project

```bash
python app.py
```

Open in browser

```
http://127.0.0.1:5000
```

---

#  Screenshots

> Add screenshots here after completing the UI.

- Home Page
- Login
- Dashboard
- Interview Page
- Result Page

---

# 🎯 Current Features

- ✅ Authentication
- ✅ AI Question Generation
- ✅ AI Interview Evaluation
- ✅ Dashboard
- ✅ Interview History
- ✅ PDF Reports
- ✅ Responsive UI
- ✅ Progress Tracking

---

# 🚀 Upcoming Features

- Coding Interview Module
- Voice Interview
- Company-specific Interview Modes
- Analytics Dashboard
- Performance Charts
- Dark Mode
- Admin Dashboard
- Email Notifications
- Leaderboard
- AI Resume Analyzer

---

# 📈 Git Workflow

This project follows a feature branch workflow.

```
main
│
develop
│
feature/interview-session
feature/result-dashboard
feature/coding-module
```

#  License

This project is developed for educational and portfolio purposes.

---

#  Developer

**Sri Vennela Marri**

B.Tech Computer Science Engineering

Python | Flask | AI | Web Development

GitHub:
https://github.com/Vennela-ai