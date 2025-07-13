from typing import List, TypedDict
from agents import function_tool

class DailyWorkout(TypedDict):
    day: str
    workout: str

@function_tool
def recommend_workout(goal_type: str, experience_level: str) -> List[DailyWorkout]:
    """Suggest a weekly workout plan based on fitness goal and experience"""

    if goal_type == "weight_loss" and experience_level == "beginner":
        return [
            {"day": "Monday", "workout": "30 min brisk walk"},
            {"day": "Tuesday", "workout": "Bodyweight strength training"},
            {"day": "Wednesday", "workout": "Rest or light yoga"},
            {"day": "Thursday", "workout": "Cardio (jump rope / cycling)"},
            {"day": "Friday", "workout": "Core workout"},
            {"day": "Saturday", "workout": "Full-body stretching"},
            {"day": "Sunday", "workout": "Rest"}
        ]
    
    if goal_type == "weight_gain" and experience_level == "intermediate":
        return [
            {"day": "Monday", "workout": "Chest + Triceps"},
            {"day": "Tuesday", "workout": "Back + Biceps"},
            {"day": "Wednesday", "workout": "Legs"},
            {"day": "Thursday", "workout": "Shoulders"},
            {"day": "Friday", "workout": "Full body strength"},
            {"day": "Saturday", "workout": "Active rest (walk, stretch)"},
            {"day": "Sunday", "workout": "Rest"}
        ]

    if goal_type == "general_fitness" and experience_level == "advanced":
        return [
            {"day": "Monday", "workout": "HIIT + Core"},
            {"day": "Tuesday", "workout": "Strength Training"},
            {"day": "Wednesday", "workout": "Yoga + Mobility"},
            {"day": "Thursday", "workout": "Cardio + Endurance"},
            {"day": "Friday", "workout": "CrossFit or Bootcamp"},
            {"day": "Saturday", "workout": "Pilates or Dance"},
            {"day": "Sunday", "workout": "Rest"}
        ]
    
    return [
        {"day": "Monday", "workout": "Walk 30 mins"},
        {"day": "Tuesday", "workout": "Stretching"},
        {"day": "Wednesday", "workout": "Bodyweight workout"},
        {"day": "Thursday", "workout": "Rest"},
        {"day": "Friday", "workout": "Cardio"},
        {"day": "Saturday", "workout": "Yoga"},
        {"day": "Sunday", "workout": "Rest"}
    ]