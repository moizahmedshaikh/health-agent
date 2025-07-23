from typing import Optional
import chainlit as cl
from all_agents import escalation_agent, injury_support_agent, nutrition_expert_agent
from main_agent import health_wellness_agent
from context import UserSessionContext
from agents import Agent, InputGuardrailTripwireTriggered, Runner
from configure_gemini import config
from hooks.agent_hooks import on_agent_start_handler, on_agent_end_handler

SWITCH_BACK_TRIGGERS = [
    "switch me back",
    "return to planner",
    "go back to health planner",
    "go back to main agent",
    "change agent to health wellness planner"
]

MAX_HISTORY_LENGTH = 10 

@cl.on_chat_start
async def on_chat_start():
    """Initialize session and agents."""
    cl.user_session.set("chat_history", [])
    cl.user_session.set("context", UserSessionContext(name="Moiz Ahmed", uid=1))
    
    # Register all agents
    cl.user_session.set("current_agent", health_wellness_agent)
    cl.user_session.set("all_agents", {
        "main": health_wellness_agent,
        "escalation": escalation_agent,
        "nutrition": nutrition_expert_agent,
        "injury": injury_support_agent
    })

    # Welcome message
    welcome_msg = """👋 Hi! I'm your health coach. Tell me your wellness goals - fitness, nutrition, or mental wellbeing.

Examples:
- "Help me lose 10kg"
- "Suggest vegetarian meal plans"
- "Create a home workout routine"

Where shall we begin?"""
    await cl.Message(content=welcome_msg).send()

@cl.on_message
async def handle_on_message(message: cl.Message):
    """Handle user messages with agent routing."""
    history = cl.user_session.get("chat_history", [])
    context = cl.user_session.get("context")
    current_agent: Optional[Agent] = cl.user_session.get("current_agent") or health_wellness_agent
    
    user_input = message.content.strip().lower()
    msg = cl.Message(content="")
    await msg.send()

    if user_input in SWITCH_BACK_TRIGGERS:
        cl.user_session.set("current_agent", health_wellness_agent)
        await cl.Message(content="🔁 Switched back to Health & Wellness Planner").send()
        return

    try:
        await on_agent_start_handler(history)

        result = Runner.run_streamed(
            starting_agent=current_agent,
            input=[*history, {"role": "user", "content": message.content}],  # Include new message
            context=context,
            run_config=config
        )

        async for event in result.stream_events():
            if event.type == "input_guardrail_triggered_event":
                output_info = getattr(event.data, "output_info", None) or  getattr(getattr(event.data, "data", None), "output_info", None)
                reason = output_info or "⚠️ Please provide clearer health goals."
                await msg.stream_token(f"🛡️ {reason}")
                return  

            elif event.type == "agent_updated_stream_event":
                cl.user_session.set("current_agent", event.new_agent)
                print(f"Agent switched to: {event.new_agent.name}")
                
                switch_msg = getattr(event.new_agent, "switch_message", f"🔄 Switched to {event.new_agent.name}")
                await cl.Message(content=switch_msg).send()

            elif event.type == "raw_response_event" and hasattr(event.data, "delta"):
                await msg.stream_token(event.data.delta)

            elif event.type == "run_item_stream_event" and event.item.type == "tool_call_output_item":
                output = event.item.output
                if isinstance(output, dict):
                    formatted = "\n".join(
                        f"**{k.replace('_', ' ').title()}**: {v}" 
                        for k, v in output.items()
                    )
                else:
                    formatted = str(output)
                await cl.Message(content=formatted).send()

        history.extend([
            {"role": "user", "content": message.content},
            {"role": "assistant", "content": msg.content}
        ])
        cl.user_session.set("chat_history", history[-MAX_HISTORY_LENGTH:])
        await on_agent_end_handler(msg.content)

    except InputGuardrailTripwireTriggered as e:
        await msg.stream_token(f"🛡️ {e.guardrail_result.output.output_info}")
    except Exception as e:
        await msg.stream_token(f"❌ Error: {str(e)}")
        print(f"System error: {e}") 
    
    await msg.update() 