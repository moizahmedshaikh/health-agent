import re
from typing import TypedDict
from agents import function_tool

class Goal(TypedDict):
    goal_type: str
    amount: float
    unit: str
    duration: str


@function_tool
def analyze_goal(input_text: str)-> Goal:
    """Analyze the user's health goal and return structured format"""
    text = input_text.lower()

    amount_unit_match = re.search(r"(\d+)\s?(kg|kgs|pounds|lbs)", text)
    duration_match = re.search(r"(in|for)?\s?(\d+)\s?(month|months|week|weeks|day|days)", text)

    if not amount_unit_match:
        raise ValueError("Missing weight amount/unit. Please say something like 'lose 5kg'.")
    
    if not duration_match:
        raise ValueError("Missing duration. Please say something like 'in 2 months'.")


    if amount_unit_match:
        amount = float(amount_unit_match.group(1))
        unit = amount_unit_match.group(2)
    else:
        amount = 0
        unit = "kg"
        

    if duration_match:
        duration = f"{duration_match.group(2)} {duration_match.group(3)}"
    else:
        duration = "unspecified"

    
    if "gain" in text:
        goal_type = "weight_gain"
    elif "loss" in text or "lose" in text or "kam" in text or "reduce" in text:
        goal_type = "weight_loss"
    else:
        goal_type = "general_fitness"

    return {
        "goal_type": goal_type,
        "amount": amount,
        "unit": unit,
        "duration": duration
    }