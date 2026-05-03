from fastapi import APIRouter
from utils.database import get_db
from routes.upload import analysis_store

router = APIRouter()


def get_latest_analysis():
    db = get_db()
    if db is not None:
        try:
            doc = db.current_analysis.find_one({}, {"_id": 0})
            if doc:
                return doc.get("analysis", {})
        except:
            pass
    return analysis_store.get("latest", {})


@router.get("/insights/")
async def get_insights():
    analysis = get_latest_analysis()

    # Pull fields with defaults
    pattern_analysis = analysis.get("pattern_analysis", {
        "summary": "Analysis of the last 10 exam cycles indicates a significant shift towards Entropy Generation Minimization and Irreversible Thermodynamics. These topics now comprise approximately 45% of the total weighted marks.",
        "tags": ["Phase-Equilibrium (Critical)", "Turbine Efficiency Patterns"]
    })

    high_yield_topics = analysis.get("high_yield_topics", [
        {"name": "Second Law Analysis", "frequency": 92, "priority": "HIGH"},
        {"name": "Combustion Stoichiometry", "frequency": 78, "priority": "HIGH"},
        {"name": "Psychrometric Applications", "frequency": 65, "priority": "MODERATE"},
        {"name": "Exergy Destruction", "frequency": 54, "priority": "MODERATE"},
    ])

    topics = analysis.get("topics", [
        {"name": "Chemical Potential Equilibrium", "importance_score": 9.5, "avg_marks": 15.5, "last_appearance": "Dec 2023", "trend": "up"},
        {"name": "Nozzle and Diffuser Flows", "importance_score": 8.2, "avg_marks": 12.0, "last_appearance": "June 2023", "trend": "flat"},
        {"name": "Reciprocating Compressors", "importance_score": 4.5, "avg_marks": 8.0, "last_appearance": "Dec 2022", "trend": "down"},
        {"name": "Gas Power Cycles (Advanced)", "importance_score": 7.0, "avg_marks": 10.5, "last_appearance": "June 2023", "trend": "up"},
    ])

    ai_insight = analysis.get("ai_insight", {
        "title": "Focus on 'Vector Calculus' this week.",
        "description": "Based on 5 years of exam trends, this topic has appeared in 80% of final papers but currently ranks as your lowest performance area."
    })

    return {
        "pattern_analysis": pattern_analysis,
        "high_yield_topics": high_yield_topics,
        "topics": topics,
        "ai_insight": ai_insight
    }
