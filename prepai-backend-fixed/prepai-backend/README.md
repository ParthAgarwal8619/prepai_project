# PrepAI Backend

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 3. Open the frontend HTML file in browser
# (prepai-frontend.html)
```

## All Working Routes

| Method | URL | Description |
|--------|-----|-------------|
| POST | /upload/ | Upload PDF papers for analysis |
| GET | /topics/ | Get topic list & weak areas |
| GET | /insights/ | Get AI pattern analysis |
| GET | /practice/?topic=Name | Get practice questions |
| GET | /study_plan/ | Get weekly study schedule |
| GET | /analyze/ | Get current analysis status |
| GET | /docs | FastAPI auto-generated API docs |

## Fixing Tesseract (for scanned PDFs)

Without Tesseract, scanned PDFs are skipped but the app still works.

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default path
3. Uncomment `TESSERACT_PATH` in `.env`

## Environment Variables (.env)

```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash
MONGO_URI=mongodb://localhost:27017
DB_NAME=prepai
```
