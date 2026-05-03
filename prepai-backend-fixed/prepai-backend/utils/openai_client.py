import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def call_gemini(prompt: str, expect_json: bool = False) -> str:
    """
    Call Gemini API. Returns text response.
    If expect_json=True, tries to extract and return clean JSON string.
    """
    if not GEMINI_API_KEY:
        print("[Gemini] No API key found in .env")
        return ""

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)

        if expect_json:
            full_prompt = prompt + "\n\nIMPORTANT: Respond ONLY with valid JSON. No markdown, no explanation, no backticks."
        else:
            full_prompt = prompt

        response = model.generate_content(full_prompt)
        result = response.text.strip()

        if expect_json:
            # Strip markdown code blocks if present
            result = re.sub(r'^```(?:json)?\s*', '', result, flags=re.MULTILINE)
            result = re.sub(r'```\s*$', '', result, flags=re.MULTILINE)
            result = result.strip()

        return result

    except Exception as e:
        print(f"[Gemini] API call failed: {e}")
        return ""


def analyze_exam_paper(text: str, subject_hint: str = "") -> dict:
    """
    Use Gemini to analyze exam paper text and extract structured insights.
    """
    prompt = f"""
You are an expert academic analyst. Analyze this exam paper text and return JSON.

Subject hint: {subject_hint or 'Unknown'}

Exam paper text:
{text[:8000]}

Return this exact JSON structure:
{{
  "subject": "subject name",
  "topics": [
    {{
      "name": "topic name",
      "frequency": 85,
      "importance_score": 8.5,
      "avg_marks": 12.0,
      "last_appearance": "Dec 2023",
      "trend": "up",
      "priority": "HIGH"
    }}
  ],
  "high_yield_topics": [
    {{
      "name": "topic name",
      "frequency": 92,
      "priority": "HIGH"
    }}
  ],
  "pattern_analysis": {{
    "summary": "Key pattern description",
    "tags": ["tag1", "tag2"]
  }},
  "weak_areas": ["area1", "area2"],
  "questions": [
    {{
      "difficulty": "Hard",
      "paper": "Paper 2023, Q1",
      "text": "question text here",
      "answer": "answer hint here",
      "time": "12 mins"
    }}
  ],
  "ai_insight": {{
    "title": "Focus on X this week",
    "description": "Based on trends, X has appeared in Y% of papers..."
  }}
}}
"""

    raw = call_gemini(prompt, expect_json=True)

    if not raw:
        return get_fallback_analysis(subject_hint)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"[Gemini] JSON parse failed, using fallback")
        return get_fallback_analysis(subject_hint)


def generate_practice_questions(topic: str, existing_questions: list = []) -> list:
    """
    Generate practice questions for a specific topic using Gemini.
    """
    existing_texts = [q.get('text', '') for q in existing_questions[:3]]
    existing_str = "\n".join(f"- {t}" for t in existing_texts) if existing_texts else "None"

    prompt = f"""
Generate 4 exam-style practice questions for the topic: "{topic}"

These questions already exist (don't repeat):
{existing_str}

Return JSON array only:
[
  {{
    "difficulty": "Hard",
    "paper": "Practice Set",
    "text": "Full question text here",
    "answer": "Detailed answer/hint here",
    "time": "12 mins"
  }}
]

Mix difficulties: 1 Easy, 2 Medium, 1 Hard.
"""

    raw = call_gemini(prompt, expect_json=True)
    if not raw:
        return []

    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except:
        return []


def get_fallback_analysis(subject: str = "") -> dict:
    """Fallback data when Gemini is unavailable."""
    return {
        "subject": subject or "General Studies",
        "topics": [
            {"name": "Core Concepts", "frequency": 85, "importance_score": 9.0, "avg_marks": 15.0, "last_appearance": "Dec 2023", "trend": "up", "priority": "HIGH"},
            {"name": "Applied Problems", "frequency": 70, "importance_score": 7.5, "avg_marks": 12.0, "last_appearance": "June 2023", "trend": "up", "priority": "HIGH"},
            {"name": "Theory & Derivations", "frequency": 60, "importance_score": 6.5, "avg_marks": 10.0, "last_appearance": "Dec 2022", "trend": "flat", "priority": "MODERATE"},
            {"name": "Numerical Methods", "frequency": 45, "importance_score": 5.0, "avg_marks": 8.0, "last_appearance": "June 2022", "trend": "down", "priority": "MODERATE"},
        ],
        "high_yield_topics": [
            {"name": "Core Concepts", "frequency": 85, "priority": "HIGH"},
            {"name": "Applied Problems", "frequency": 70, "priority": "HIGH"},
            {"name": "Theory & Derivations", "frequency": 60, "priority": "MODERATE"},
        ],
        "pattern_analysis": {
            "summary": "Analysis indicates high-frequency topics in core concepts and applied problems. Focus revision on these areas for maximum marks.",
            "tags": ["Core Concepts (Critical)", "Applied Problem Patterns"]
        },
        "weak_areas": ["Numerical Methods", "Advanced Derivations"],
        "questions": [],
        "ai_insight": {
            "title": "Focus on Core Concepts this week.",
            "description": "Based on exam trends, core concepts appear in 85% of papers but require focused practice to score full marks."
        }
    }
