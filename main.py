# import os
# from dotenv import load_dotenv
# from agents import OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI


# load_dotenv()

# gemini_key = os.getenv("GEMINI_API_KEY")

# client = AsyncOpenAI(
#     api_key=gemini_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=client
# )

# config = RunConfig(
#     model=model,
#     tracing_disabled=True
# )











import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from tools.goal_analyzer import analyze_goal
from tools.meal_planner import generate_meal_planner
from tools.shedule import schedule_checkin
from tools.tracker import track_progress
from tools.workout_recommender import recommend_workout
# from agent.escalation_agent import get_escalation_agent
# from agent.nutrition_expert_agent import get_nutrition_expert_agent
# from agent.injury_support_agent import get_injury_support_agent
from all_agents.escalation_agent import get_escalation_agent
from all_agents.injury_support_agent import get_injury_support_agent
from all_agents.nutrition_expert_agent import get_nutrition_expert_agent
# from chat_collections.db import chat_collection
from datetime import datetime
# from guardrails. import on_user_message
# from guardrails.output_filter import validate_agent_output
from all_guardrails.input_validation import on_user_message
from all_guardrails.output_validation import validate_agent_output
from lifecycle_hooks.on_agent_start import on_agent_start_handler
from lifecycle_hooks.on_agent_end import on_agent_end_handler



load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please define it in your .env file.")

@cl.on_chat_start
async def start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)

    agent: Agent = Agent(
        name="Health and Wellness Agent",
        instructions="""
# Role: Health & Wellness Planner

You are a **friendly AI wellness coach** specializing in fitness, nutrition, and mental well-being.  
Your tone is **warm, supportive, and professional** (use emojis occasionally 😊).  

---

## 🧠 Core Responsibilities

1. **Goal Collection & Analysis**  
   - Use the `GoalAnalyzerTool` to understand and structure the user's goals.  
   - Ask about:
     - Fitness goals (e.g., weight loss, muscle gain, stamina)
     - Dietary preferences (vegetarian, vegan, allergies)
     - Mental wellness (stress levels, sleep patterns)
   - Example: *"What's your target weight? 🎯"*

2. **Personalized Planning**  
   - Use `MealPlannerTool` to generate a 7-day meal plan based on preferences and goals.  
   - Use `WorkoutRecommenderTool` to suggest a weekly workout routine (home/gym options).  
   - Always confirm preferences: *"Should I include yoga for stress relief? 🧘"*  

3. **Progress Support**  
   - Use `ProgressTrackerTool` to accept updates and track user milestones.  
   - Use `CheckinSchedulerTool` to schedule recurring weekly check-ins.  
   - Example: *"How's your progress going with those 10k daily steps? 🚶‍♀️"*  

4. **Handoff Protocol**  
   - Escalate or refer the user when special needs arise:
     - Request for human coach → `EscalationAgent`: *"Connecting you to a real coach... 🚸"*
     - Special dietary needs (e.g. diabetes, gluten-free) → `NutritionExpertAgent`: *"Let me bring in a nutrition expert 🍏"*
     - Physical pain or injury → `InjurySupportAgent`: *"Let me get you safety tips 🩹"*

5. **Safety & Ethics**  
   - Never give medical diagnoses.  
   - Always add a disclaimer: *"Please consult a doctor before starting any new workouts or diets. ⚠️"*

---

## 📌 Tip
Use the available tools (functions) to automate and enhance planning, scheduling, and tracking for each user. Rely on tool calls instead of freeform guessing when possible.
        """,
        model=model,
        tools=[analyze_goal, generate_meal_planner, schedule_checkin, track_progress, recommend_workout],
        handoffs=[get_escalation_agent, get_nutrition_expert_agent, get_injury_support_agent]
    )

    cl.user_session.set("agent", agent)
    cl.user_session.set("escalation_agent", get_escalation_agent(model))
    cl.user_session.set("nutrition_expert_agent", get_nutrition_expert_agent(model))
    cl.user_session.set("injury_support_agent", get_injury_support_agent(model))

    welcome_msg = """👋 Hi! I'm your health coach. Tell me your wellness goals - fitness, nutrition, or mental wellbeing. 

Examples:
"Help me lose 10kg"
"Suggest vegetarian meal plans"
"Create a home workout routine"

Where shall we begin?"""

    await cl.Message(content=welcome_msg).send()

@cl.on_message
async def main(message: cl.Message):
    if not await on_user_message(message):
        return

    history = cl.user_session.get("chat_history") or []
    msg = cl.Message(content="")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    try:
        await on_agent_start_handler(history)

        history.append({"role": "user", "content": message.content})
        result = Runner.run_streamed(agent, history, run_config=config)

        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)

        history.append({"role": "assistant", "content": msg.content})
        cl.user_session.set("chat_history", history)

        msg.content = validate_agent_output(msg.content)
        await msg.update()

        # chat_collection.insert_one({
        #     "user_message": message.content,
        #     "assistant_reply": msg.content,
        #     "timestamp": datetime.utcnow()
        # })

        await on_agent_end_handler(msg.content)

        print(f"User: {message.content}")
        print(f"Assistant: {msg.content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.send()
        print(f"Error: {str(e)}")