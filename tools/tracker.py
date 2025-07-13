from typing import TypedDict
from datetime import datetime
from agents import function_tool


class ProgressLog(TypedDict):
    date: str       # e.g., "11 July 2025"
    update: str     # e.g., "Lost 1kg"

@function_tool
def track_progress(update: str) -> ProgressLog :
    """
    Log user's progress with date
    """

    today = datetime.now().strftime("%d %B %Y")

    return {
        "date": today,
        "update": update
    }