from agents import function_tool, Agent, Runner, RunContextWrapper
from typing import Optional
from pydantic import BaseModel
from context import UserSessionContext
from configure_gemini import *


class CheckinSchedule(BaseModel):
    frequency: str
    day: Optional[str]


scheduler_agent = Agent(
    name="Check-in Scheduler Agent",
    instructions=(
        "Schedule a check-in for the user based on their goal. "
        "Suggest a check-in frequency like 'weekly' or 'every 3 days'. "
        "If weekly, also specify a day. Return result as JSON in this format:\n"
        '{\n  "frequency": "weekly",\n  "day": "Monday"\n}'
    ),
    output_type=CheckinSchedule
)


@function_tool
async def schedule_checkin(ctx: RunContextWrapper[UserSessionContext]) -> str:
    """
    Suggests check-in schedule (like weekly reminders) based on user goals.
    Returns a user-friendly message.
    """

    # 🔒 Fallback if goal is None
    user_goal = ctx.context.goal or {
        "goal_type": "general_fitness",
        "quantity": None,
        "duration": "2 weeks"
    }

    prompt = f"Suggest a check-in reminder schedule for goal: {user_goal}"

    result = await Runner.run(
        starting_agent=scheduler_agent,
        input=prompt,
        context=ctx.context,
        run_config=config
    )

    schedule = result.final_output

    # 🧠 Save to progress logs
    ctx.context.progress_logs.append({
        "type": "checkin_schedule",
        "frequency": schedule.frequency,
        "day": schedule.day or ""
    })

    # ✅ Friendly response for user
    if schedule.frequency.lower() == "weekly" and schedule.day:
        return f"✅ I've scheduled weekly check-ins for you every **{schedule.day}**. Stay consistent! 📆"
    else:
        return f"✅ Your check-ins are scheduled **{schedule.frequency}**. Let's keep up the momentum! 🔁"
