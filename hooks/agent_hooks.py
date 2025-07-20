from typing import Any
from agents import Agent, RunContextWrapper, RunHooks, AgentHooks

class TestHook(RunHooks):
    def __init__(self):
        self.event_counter = 0
        self.name = "TestHook"

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent)-> None:
        self.event_counter += 1
        print(f"### HookName: {self.name}, Counts: {self.event_counter}, Agent: {agent.name} started. Usage: {context.usage}")

