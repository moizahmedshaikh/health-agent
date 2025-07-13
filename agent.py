# import asyncio
# from agents import Agent, ItemHelpers, Runner
# from tools.goal_analyzer import *
# from tools.meal_planner import *
# from tools.workout_recommender import recommend_workout
# from tools.shedule import schedule_checkin
# from tools.reminder import check_for_checkin_reminder
# from tools.tracker import track_progress
# from context import UserSessionContext
# from agents import RunContextWrapper
# from guardrails import *
# from lifecycle_hooks.hooks import HealthCoachHook
# from main import *


# # meal_tool_with_guardrail = generate_meal_planner.with_output_guardrail(meal_output_guardrail)

# agent = Agent(
#     name="HealthAgent",
#     instructions="""
# You are a helpful digital health coach. Guide users through their health and wellness goals by asking questions,
# understanding their needs, and calling the right tools (e.g., goal analyzer, meal planner, workout suggester, progress tracker, etc.).
# Keep conversation supportive and motivating.
# """,
#     tools=[
#         analyze_goal,
#         recommend_workout,
#         schedule_checkin,
#         check_for_checkin_reminder,
#         track_progress,
#         generate_meal_planner
#         # meal_tool_with_guardrail
#     ],
#     input_guardrails=[goal_input_guardrail],
#     hooks=HealthCoachHook()
# )

# context = RunContextWrapper(
#     context=UserSessionContext(name="Moiz Ahmed", uid=1)
# )


# async def main():
#     try:
#         print("🚀 Health & Wellness Session Starting...\n")

#         result = Runner.run_streamed(
#             starting_agent=agent,
#             input="Mujhe weight gain karna hai aur workout plan bhi chahiye",
#             context=context,
#             run_config=config
#         )

#         async for event in result.stream_events():
#             # Skip token-by-token raw stream
#             if event.type == "raw_response_event":
#                 continue

#             # Jab agent switch ho (handoff)
#             elif event.type == "agent_updated_stream_event":
#                 print(f"\n🧠 Agent switched to: {event.new_agent.name}\n")

#             # Jab kuch naya generate ho
#             elif event.type == "run_item_stream_event":
#                 if event.item.type == "tool_call_item":
#                     print("🔧 Tool called...")
#                 elif event.item.type == "tool_call_output_item":
#                     print(f"✅ Tool output: {event.item.output}")
#                 elif event.item.type == "message_output_item":
#                     print(f"💬 AI Response:\n{ItemHelpers.text_message_output(event.item)}")

#         print("\n🏁 Session Completed.")

#     except Exception as e:
#         fallback_message = getattr(context.context, "last_error", None)
#         if fallback_message:
#             print("🤖 Health Agent:", fallback_message)
#         else:
#             print("❌ Unexpected Error:", str(e))

# asyncio.run(main())