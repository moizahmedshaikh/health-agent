# from unittest import result
# from dotenv import load_dotenv
# import os
# from agents import Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
# from context import UserSessionContext
# from main_agent import health_wellness_agent
# import asyncio
# from utils.streaming import stream_response
# from configure_gemini import *


# user_context  = UserSessionContext(name="Moiz Ahmed", uid=1)

# async def main():
#     while True:
#         user_input = input("👤 You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             break
#         await stream_response(health_wellness_agent, user_input, user_context, config)



# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except Exception as e:
#         import traceback
#         print("🔥 ERROR:", traceback.format_exc())