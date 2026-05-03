from pydantic import BaseModel
from typing import List, Optional

class TopicModel(BaseModel):
    name: str
    frequency: Optional[int] = 0
    importance_score: Optional[float] = 0.0
    avg_marks: Optional[float] = 0.0
    last_appearance: Optional[str] = ""
    trend: Optional[str] = "flat"
    priority: Optional[str] = "MODERATE"

class AnalysisResult(BaseModel):
    subject: str
    total_topics: int
    high_priority_count: int
    topics: List[TopicModel]
    weak_areas: List[str]

class QuestionModel(BaseModel):
    difficulty: str
    paper: str
    text: str
    answer: Optional[str] = ""
    time: Optional[str] = "10 mins"
    source: Optional[str] = ""
