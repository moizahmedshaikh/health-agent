from agents import RunContextWrapper
from pydantic import BaseModel
from typing import Optional, Dict, List

class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = []
    checkin_day: Optional[str] = "Friday"
    last_error: str = None
