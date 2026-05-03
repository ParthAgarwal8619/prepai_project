import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from utils.pdf_extractor import extract_text_from_pdf
from utils.question_parser import extract_topics_from_text, parse_questions_from_text
from utils.openai_client import analyze_exam_paper
from utils.database import get_db

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory store (fallback if MongoDB is down)
analysis_store = {}


@router.post("/upload/")
async def upload_papers(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    all_text = ""
    file_names = []
    saved_paths = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            continue

        save_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        saved_paths.append(save_path)
        file_names.append(file.filename)

        text = extract_text_from_pdf(save_path)
        all_text += f"\n\n--- FILE: {file.filename} ---\n\n{text}"

    if not all_text.strip():
        # PDFs were scanned and OCR unavailable - still analyze with filename hints
        subject_hint = " ".join(file_names)
        all_text = f"Exam papers: {subject_hint}"

    # Detect subject from filenames
    subject_hint = detect_subject(file_names)

    # Run AI analysis
    print(f"[Analysis] Running AI analysis on {len(file_names)} file(s)...")
    analysis = analyze_exam_paper(all_text, subject_hint)

    # Store result
    db = get_db()
    if db is not None:
        try:
            db.analyses.insert_one({"files": file_names, "analysis": analysis})
            db.current_analysis.drop()
            db.current_analysis.insert_one({"analysis": analysis, "files": file_names})
        except Exception as e:
            print(f"[DB] Write error: {e}")

    # Always keep in-memory copy
    analysis_store["latest"] = analysis
    analysis_store["files"] = file_names

    return {
        "status": "success",
        "files_processed": len(file_names),
        "subject": analysis.get("subject", subject_hint),
        "topics_found": len(analysis.get("topics", [])),
        "message": "Analysis complete"
    }


def detect_subject(filenames: List[str]) -> str:
    text = " ".join(filenames).lower()
    if any(k in text for k in ["math", "calculus", "algebra"]): return "Mathematics"
    if any(k in text for k in ["physics", "quantum", "thermal", "thermo"]): return "Physics / Thermodynamics"
    if any(k in text for k in ["cs", "computer", "programming"]): return "Computer Science"
    if any(k in text for k in ["chem", "organic", "inorganic"]): return "Chemistry"
    return "General Science"
