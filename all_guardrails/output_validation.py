def validate_agent_output(text: str) -> str:
    sensitive_keywords = ["workout", "diet", "fasting"]
    if any(word in text.lower() for word in sensitive_keywords):
        text += "\n\n⚠️ *Please consult a doctor or professional before following this advice.*"

    return text