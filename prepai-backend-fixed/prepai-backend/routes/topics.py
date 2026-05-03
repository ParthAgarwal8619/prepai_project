from fastapi import APIRouter
from utils.database import get_db
from routes.upload import analysis_store

router = APIRouter()


def get_latest_analysis():
    # Try DB first
    db = get_db()
    if db is not None:
        try:
            doc = db.current_analysis.find_one({}, {"_id": 0})
            if doc:
                return doc.get("analysis", {})
        except:
            pass
    # Fallback to memory
    return analysis_store.get("latest", {})


@router.get("/topics/")
async def get_topics():
    analysis = get_latest_analysis()

    topics = analysis.get("topics", [])
    weak_areas = analysis.get("weak_areas", [])

    # Format weak areas as objects if they're strings
    weak_area_objs = []
    for w in weak_areas:
        if isinstance(w, str):
            weak_area_objs.append({"name": w})
        else:
            weak_area_objs.append(w)

    high_priority = [t for t in topics if t.get("priority") == "HIGH"]

    return {
        "total": len(topics) if topics else 42,
        "high_priority": len(high_priority) if high_priority else 8,
        "topics": topics or get_demo_topics(),
        "weak_areas": weak_area_objs or [
            {"name": "Quantum Mechanics II"},
            {"name": "Advanced Thermodynamics"},
            {"name": "Electromagnetic Theory"},
        ]
    }


def get_demo_topics():
    return [
        {"name": "Topic A", "frequency": 85},
        {"name": "Topic B", "frequency": 60},
        {"name": "Topic C", "frequency": 40},
        {"name": "Topic D", "frequency": 95},
        {"name": "Topic E", "frequency": 50},
        {"name": "Topic F", "frequency": 70},
    ]
