from typing import cast
import chainlit as cl
from all_agents import escalation_agent, injury_support_agent, nutrition_expert_agent
from main_agent import health_wellness_agent
from context import UserSessionContext
from agents import Agent, InputGuardrailTripwireTriggered, Runner
from configure_gemini import *

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    cl.user_session.set("context", UserSessionContext(name="Moiz Ahmed", uid=1))

    cl.user_session.set("agent", health_wellness_agent)
    cl.user_session.set("escalation_agent", escalation_agent)
    cl.user_session.set("nutrition_expert_agent", nutrition_expert_agent)
    cl.user_session.set("injury_support_agent", injury_support_agent)

    cl.user_session.set("current_agent", health_wellness_agent)
    cl.user_session.set("previous_agent", health_wellness_agent)

    welcome_msg = """👋 Hi! I'm your health coach. Tell me your wellness goals - fitness, nutrition, or mental wellbeing.

Examples:
- "Help me lose 10kg"
- "Suggest vegetarian meal plans"
- "Create a home workout routine"

Where shall we begin?"""
    await cl.Message(content=welcome_msg).send()


@cl.on_message
async def handle_on_message(message: cl.Message):
    history = cl.user_session.get("chat_history") or []
    contx = cl.user_session.get("context")
    agent = cast(Agent, cl.user_session.get("current_agent"))

    msg = cl.Message(content="")
    await msg.send()

    try:
        history.append({"role": "user", "content": message.content})

        result = Runner.run_streamed(
            agent,
            input=history,
            context=contx,
            run_config=config
        )

        async for event in result.stream_events():
            if event.type == "input_guardrail_triggered_event":
                output_info = getattr(event.data, "output_info", None)
                if output_info is None and hasattr(event.data, "data"):
                    output_info = getattr(event.data.data, "output_info", None)

                reason = output_info or "⚠️ Invalid input. Please try again with a clear health goal."
                await msg.stream_token(f"🛡️ {reason}")
                await msg.update()
                return

            elif event.type == "agent_updated_stream_event":
                # Save previous agent
                cl.user_session.set("previous_agent", cl.user_session.get("current_agent"))
                # Update current agent
                cl.user_session.set("current_agent", event.new_agent)
                await cl.Message(content=f"🧠 [Agent switched to]: {event.new_agent.name}").send()

            elif event.type == "raw_response_event" and hasattr(event.data, "delta"):
                await msg.stream_token(event.data.delta)

            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    await cl.Message(content="🔧 [Tool used]").send()
                elif event.item.type == "tool_call_output_item":
                    output = event.item.output
                    if output:
                        await cl.Message(content=f"✅ [Tool output]: {output}").send()

        if message.content.lower() in ["switch me back", "return to planner"]:
            prev_agent = cl.user_session.get("previous_agent")
            cl.user_session.set("current_agent", prev_agent)
            await cl.Message(content=f"🔁 Switched back to: {prev_agent.name}").send()
            return

                    
        history.append({"role": "assistant", "content": msg.content})
        cl.user_session.set("chat_history", history)
        await msg.update()

    except InputGuardrailTripwireTriggered as e:
        reason = getattr(e, "output_info", str(e)) or "⚠️ Input blocked."
        await msg.stream_token(f"🛡️ {reason}")
        await msg.update()

    except Exception as e:
        msg.content = f"❌ Error: {str(e)}"
        await msg.send()
        print(f"Error: {str(e)}")
