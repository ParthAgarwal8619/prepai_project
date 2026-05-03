# 🚀 PrepAI – Past Paper Analyzer

## 📌 Overview

PrepAI is an AI-powered platform that analyzes past exam papers and identifies high-priority topics, helping students prepare efficiently using data-driven insights.

---

## 🎯 Features

* 📄 Upload past exam papers (PDF)
* 🤖 AI-based topic extraction (Gemini API)
* 📊 Topic frequency & trend analysis
* 🧠 Smart insights & weak area detection
* 📅 Personalized study planner
* ✍️ Practice question generation

---

## 🛠️ Tech Stack

* Frontend: HTML, CSS, JavaScript
* Backend: FastAPI (Python)
* AI: Gemini API
* Database: MongoDB

---

## ⚙️ How to Run Locally

```bash
# Go to backend folder
cd prepai-backend

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn main:app --reload
```

👉 Open API docs:
http://127.0.0.1:8000/docs

👉 Open frontend:

```bash
open prepai-frontend.html
```

---

## 🌐 Live Demo

👉 (Add your Vercel link here)

---

## 🎥 Demo Video (MANDATORY)

👉 (Add Google Drive / YouTube link here)

---

## 📡 API Routes

| Method | Endpoint     | Description        |
| ------ | ------------ | ------------------ |
| POST   | /upload/     | Upload PDFs        |
| GET    | /topics/     | Get topic analysis |
| GET    | /insights/   | AI insights        |
| GET    | /practice/   | Practice questions |
| GET    | /study_plan/ | Study plan         |
| GET    | /analyze/    | Analysis status    |

---

## ⚙️ Environment Variables (.env)

```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash
MONGO_URI=mongodb://localhost:27017
DB_NAME=prepai
```

---

## 🧪 Notes

* Tesseract required only for scanned PDFs
* App works without it for normal PDFs

---

## 📂 Project Structure

```
prepai/
 ├── prepai-backend/
 ├── prepai-frontend.html
```

---

## 👨‍💻 Developer

Parth Agrawal

---

## 📢 Hackathon Note

This project was built as part of a hackathon to demonstrate AI-powered exam analysis and intelligent study planning.
