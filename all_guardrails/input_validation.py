import chainlit as cl

async def on_user_message(message: cl.Message) -> bool:
    content = message.content.strip()

    if not content:
        await cl.Message(content="❌ Please enter a message.").send()
        return False
    
    if any(bad_word in content.lower() for bad_word in ["kill", "die", "suicide"]):
        await cl.Message(content="⚠️ Please avoid using harmful language.").send()
        return False

    return True