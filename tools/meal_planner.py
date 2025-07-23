from agents import function_tool, Agent, Runner, RunContextWrapper
from typing import List
from pydantic import BaseModel
from context import UserSessionContext
from configure_gemini import *


class MealPlanner(BaseModel):
    days: List[str]



@function_tool(name_override="meal_planner")
async def meal_planner(ctx: RunContextWrapper[UserSessionContext], diet_preference: str) -> str:
    """
    Generates a 7-day meal plan according to user diet_preference.
    """

    if diet_preference.lower() not in ["vegetarian", "non vegetarian", "non-vegetarian", "keto", "vegan"]:
        return "❌ Invalid diet preference. Please choose from: vegetarian, non-vegetarian, keto, or vegan."

    instructions = (
        f"Create a 7-day {diet_preference.lower()} meal plan in list format (one string per day). "
        f"Make sure to follow the {diet_preference.lower()} diet strictly. "
        f"Respond ONLY with a list of 7 meal suggestions."
    )

    dynamic_agent = Agent(
        name="Meal Planner Agent",
        instructions=instructions,
        output_type=MealPlanner
    )

    try:
        result = await Runner.run(
            dynamic_agent,
            input=diet_preference,
            context=ctx.context,
            run_config=config
        )

        meal_data = result.final_output  # this is MealPlanner object
        ctx.context.meal_plan = meal_data

        formatted_meals = "\n".join([f"- {day}" for day in meal_data.days])
        return f"✅ Here's your 7-day {diet_preference.lower()} meal plan:\n{formatted_meals}"

    except Exception as e:
        return f"❌ Failed to generate meal plan. Error: {str(e)}"