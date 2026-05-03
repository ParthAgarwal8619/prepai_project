from fastapi import APIRouter
from routes.upload import analysis_store
from utils.database import get_db

router = APIRouter()


@router.get("/analyze/")
async def get_analysis():
    """Return current analysis status and summary."""
    analysis = analysis_store.get("latest", {})
    files = analysis_store.get("files", [])

    return {
        "has_analysis": bool(analysis),
        "files_analyzed": files,
        "subject": analysis.get("subject", ""),
        "topics_count": len(analysis.get("topics", [])),
        "status": "ready" if analysis else "no_data"
    }
