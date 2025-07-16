# from agents import Agent, Tool, RunContextWrapper
# from typing import Any


# class HealthAgentHooks:
#     async def on_start(self, context: RunContextWrapper, agent: Agent):
#         print(f"🚀 Agent `{agent.name}` started.")

#     async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any):
#         print(f"✅ Agent `{agent.name}` ended with output: {output}")

#     async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool):
#         print(f"🛠️ Tool `{tool.name}` started.")

#     async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str):
#         print(f"📦 Tool `{tool.name}` ended with result: {result}")

#     async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent):
#         print(f"🔁 Handoff from `{source.name}` ➡️ `{agent.name}`")
