# from agents import AgentHooks
# from context import UserSessionContext
# import datetime


# class HealthCoachHook(AgentHooks):
#     async def on_agent_start(self, input: str, context: UserSessionContext):
#         print(f"[START] User '{context.name}' started a session with input: '{input}' at {datetime.datetime.now()}")
#         # You can log this or save to DB
#         return input

#     async def on_tool_start(self, tool_name: str, input: dict, context: UserSessionContext):
#         print(f"[TOOL START] {tool_name} called with input: {input}")
#         return input

#     async def on_tool_end(self, tool_name: str, input: dict, output: dict, context: UserSessionContext):
#         print(f"[TOOL END] {tool_name} responded with: {output}")
#         return output

#     async def on_agent_end(self, input: str, output: str, context: UserSessionContext):
#         print(f"[END] Session ended for user '{context.name}' with final output: '{output}'")
#         return output
    

    