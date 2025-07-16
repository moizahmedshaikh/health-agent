from agents import Runner, ItemHelpers
from context import UserSessionContext
from openai.types.responses import ResponseTextDeltaEvent

last_agent_name = None 


async def stream_response(agent, user_input: str, user_context: UserSessionContext, config):
    global last_agent_name

    try:
        result = Runner.run_streamed(
            agent,
            input=user_input,
            context=user_context,
            run_config=config
        )

        async for event in result.stream_events():
            # 1️⃣ Ignore token streaming OR enable token-by-token print
            if event.type == "raw_response_event":
                if isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
                continue

            # 2️⃣ Agent switched
            elif event.type == "agent_updated_stream_event":
                if event.new_agent.name != last_agent_name:
                    print(f"\n[Agent switched to]: {event.new_agent.name}")
                    last_agent_name = event.new_agent.name

            # 3️⃣ Tool usage and message output
            elif event.type == "run_item_stream_event":
                item = event.item
                if item.type == "tool_call_item":
                    print("\n[Tool used]")
                elif item.type == "tool_call_output_item":
                    print(f"[Tool output]: {item.output}")
                elif item.type == "message_output_item":
                    print(f"🤖 {ItemHelpers.text_message_output(item)}")

    except Exception as e:
        print(f"🔥 ERROR during streaming: {e}")
