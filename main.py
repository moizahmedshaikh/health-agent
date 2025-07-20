from agents import Agent, Runner, InputGuardrailTripwireTriggered
from context import UserSessionContext
from main_agent import health_wellness_agent
import asyncio
from utils.streaming import stream_response
from configure_gemini import *


user_context  = UserSessionContext(name="Moiz Ahmed", uid=1)

async def main():
    while True:
        # try:
            user_input = input("👤 You: ")
            if user_input.lower() in ["exit", "quit"]:
                break

        #     result = await Runner.run(
        #         starting_agent=health_wellness_agent,
        #         input=user_input,
        #         context=user_context,
        #         run_config=config
        #     )
        #     print(result.final_output)

        # except InputGuardrailTripwireTriggered as e:
        #     print(e.guardrail_result.output.output_info)

        # except Exception as e:
        #     print(f"Error: {str(e)}")

            await stream_response(health_wellness_agent, user_input, user_context=user_context, config=config)
 

if __name__ == "__main__":
    asyncio.run(main())
