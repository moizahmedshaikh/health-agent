async def on_agent_start_handler(history):
    print("🔄 [Lifecycle] Agent run started.")
    print(f"Chat history so far: {history}")


async def on_agent_end_handler(agent_reply: str):
    print("✅ [Lifecycle] Agent run completed.")
    print(f"Agent Reply: {agent_reply}")