# from typing import List, TypedDict
# from agents import Agent, Runner, GuardrailFunctionOutput, RunContextWrapper, TResponseInputItem, input_guardrail, output_guardrail
# from pydantic import BaseModel
# from main import *


# class GoalGuardrailOutput(BaseModel):
#     is_valid_goal: bool
#     reasoning: str

# guardrail_agent = Agent(
#     name="GoalGuardrailAgent",
#     instructions="Determine if the input is a valid health goal with amount, unit, and duration. Return is_valid_goal True/False and explain why.",
#     output_type=GoalGuardrailOutput,
# )


# @input_guardrail
# async def goal_input_guardrail(
#     ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput: 
    
#     result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config=config)
    
#     if not result.final_output.is_valid_goal:
#         ctx.context.last_error = result.final_output.reasoning or "Invalid health goal format."

#     return GuardrailFunctionOutput(
#         output_info=result.final_output,
#         tripwire_triggered= not result.final_output.is_valid_goal
#     )



# class DailyMeal(TypedDict):
#     day: str
#     breakfast: str
#     lunch: str
#     dinner: str


# @output_guardrail
# async def meal_output_guardrail(
#     ctx: RunContextWrapper, agent: Agent, output: List[DailyMeal]
# ) -> GuardrailFunctionOutput:
    
#     for day in output:
#         if not all([
#             isinstance(day.get("breakfast"), str) and day["breakfast"] != "Not available",
#             isinstance(day.get("lunch"), str) and day["lunch"] != "Not available",
#             isinstance(day.get("dinner"), str) and day["dinner"] != "Not available"
#         ]):
#             return GuardrailFunctionOutput(
#                 output_info={"error": "Meal plan contains missing or invalid meals"},
#                 tripwire_triggered=True
#             )
        
        
#     return GuardrailFunctionOutput(
#         output_info={"status": "Meal plan looks good"},
#         tripwire_triggered=False
#     )

