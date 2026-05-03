from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

# Import all routers
from routes import upload, topics, insights, practice, study_plan, analyze
from utils.database import connect_db

app = FastAPI(
    title="PrepAI Backend",
    description="AI-powered exam preparation backend",
    version="1.0.0"
)

# ─── CORS ────────────────────────────────────────────────────────────────────
# Allow ALL origins so the HTML file works when opened directly from disk
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── DATABASE ─────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    connect_db()
    os.makedirs("uploads", exist_ok=True)

# ─── ROUTERS ──────────────────────────────────────────────────────────────────
app.include_router(upload.router)
app.include_router(topics.router)
app.include_router(insights.router)
app.include_router(practice.router)
app.include_router(study_plan.router)
app.include_router(analyze.router)

# ─── ROOT ─────────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "app": "PrepAI Backend",
        "status": "running",
        "version": "1.0.0",
        "routes": [
            "POST /upload/",
            "GET  /topics/",
            "GET  /insights/",
            "GET  /practice/?topic=TopicName",
            "GET  /study_plan/",
            "GET  /analyze/",
        ]
    }

# ─── HEALTH CHECK ─────────────────────────────────────────────────────────────
@app.get("/health/")
async def health():
    return {"status": "ok"}
