# 🧠 StudyMind – AI Study Companion

🌐 Live Demo: https://aistudybuddy-esn7w3y6cyxbsnhmofwtb4.streamlit.app/

<img width="1366" height="677" alt="Screenshot (342)" src="https://github.com/user-attachments/assets/80fae08b-232b-46b4-a05d-694a2a2f1530" />

StudyMind is an AI-powered study assistant built with Streamlit and Google's Gemini AI. It helps students learn faster by explaining concepts, summarizing notes, generating quizzes, and creating personalized study plans.

## ✨ Features

### 💡 Explain Topics

* Explain any concept from beginner to advanced level.
* Optional real-world examples.
* Adjustable explanation depth:

  * Beginner
  * Intermediate
  * Advanced

### 📄 Smart Note Summarization

* Paste notes directly.
* Upload PDF documents.
* Generate concise summaries.
* Multiple output formats:

  * Paragraph
  * Bullet Points
  * Key-Value Format

### 📝 AI Quiz Generator

* Create quizzes from:

  * Topics
  * Notes
  * PDF documents
* Question types:

  * MCQ
  * True/False
  * Short Answer
  * Mixed
* Adjustable difficulty levels.
* Optional answer key generation.

### 📅 Personalized Study Planner

* Create day-wise study schedules.
* Based on:

  * Subjects
  * Available study days
  * Daily study hours
  * Difficulty level
  * Learning goals

### 🕘 Session History

* Stores generated outputs during the session.
* Download previous results.
* Clear history anytime.

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* HTML
* CSS

### AI

* Google Gemini API

### Python Libraries

* Streamlit
* PyPDF2
* pdfplumber
* python-dotenv
* google-generativeai

---

## 📂 Project Structure

```text
StudyMind/
│
├── app.py
├── gemini_utils.py
├── requirements.txt
├── .env
├── README.md
│
└── assets/
    ├── Home.png
    ├── Quiz.png
    └── schedule.png
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/gayathrikakumani24-droid/ai_studyBuddy.git
cd studymind
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Gemini API

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

The application will open in:

```text
http://localhost:8501
```

---

## 🚀 Deployment

This project can be deployed on:

* Streamlit Community Cloud
* Hugging Face Spaces
* Render
* Railway
* Vercel (frontend wrapper)

---

## 📸 Screenshots

Add screenshots inside the `assets` folder and reference them:
### Home

<img width="1366" height="677" alt="Screenshot (342)" src="https://github.com/user-attachments/assets/ff13f560-c751-42cc-a823-d4ffe47d50bb" />

### Quiz Generator

<img width="1366" height="637" alt="Screenshot (343)" src="https://github.com/user-attachments/assets/ab6c3008-caff-4f71-a37b-0f706b615428" />

### Study Planner

<img width="1366" height="635" alt="Screenshot (344)" src="https://github.com/user-attachments/assets/18d970bd-42d9-420d-b93a-a18e98ac60f4" />


---

## 🎯 Future Improvements

* User authentication
* Export to PDF
* Dark mode
* Flashcards
* Progress tracking
* Learning analytics

---

## 👩‍💻 Author

Gayathri

Computer Science & Engineering (AI & ML)

Built with ❤️ using Streamlit and Gemini AI.
