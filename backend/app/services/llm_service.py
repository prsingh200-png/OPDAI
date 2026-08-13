from app.config import get_settings
from app.prompts.summary_prompt import SUMMARY_SYSTEM_PROMPT
from app.utils.logger import get_logger

logger = get_logger(__name__)

def generate_summary(symptoms: str, prescription_text: str = "") -> str:
    settings = get_settings()
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured. Add it to backend/.env.")

    from openai import OpenAI
    client = OpenAI(api_key=settings.openai_api_key)

    user_input = f"""
Patient-reported symptoms:
{symptoms}

Uploaded prescription text:
{prescription_text or "No prescription uploaded."}
"""

    response = client.responses.create(
        model=settings.openai_model,
        instructions=SUMMARY_SYSTEM_PROMPT,
        input=user_input,
    )
    text = response.output_text.strip()
    logger.info("Generated AI summary")
    return text
