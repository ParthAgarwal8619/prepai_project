from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/study_plan/")
async def get_study_plan():
    today = datetime.now()
    week_days = []
    for i in range(7):
        day = today + timedelta(days=i - today.weekday())
        week_days.append({
            "name": day.strftime("%a").upper(),
            "num": day.day,
            "is_today": day.date() == today.date()
        })

    return {
        "daily_goal_percent": 70,
        "week": week_days,
        "sessions": [
            {
                "title": "Morning Deep Work: Fluid Dynamics",
                "time": "09:00 AM – 11:30 AM",
                "subtitle": "Focusing on Laminar Flow Equations",
                "status": "IN PROGRESS"
            },
            {
                "title": "Past Paper Review: 2022 Session",
                "time": "02:00 PM – 04:00 PM",
                "subtitle": "Analysis of Section B",
                "status": "UPCOMING"
            }
        ],
        "ai_actions": [
            {"priority": "HIGH", "title": "Re-solve problem 4c from 2021 Finals", "subtitle": "Based on common failure patterns", "done": False},
            {"priority": "MEDIUM", "title": "Review Thermodynamic Laws", "subtitle": "Found weak link in Chapter 3 concepts", "done": True},
            {"priority": "LOW", "title": "Organize revision flashcards", "subtitle": "Prep for tomorrow's flash-round", "done": False},
        ],
        "performance_predictor": {
            "mastery_percent": 82,
            "focus_topic": "entropy calculations",
            "boost_percent": 5
        }
    }
