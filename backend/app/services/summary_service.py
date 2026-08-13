from app.services.llm_service import generate_summary
from app.services.upload_service import extract_text_from_upload

def create_summary(symptoms: str, prescription_path: str | None = None) -> str:
    prescription_text = ""
    if prescription_path:
        prescription_text = extract_text_from_upload(prescription_path)
    return generate_summary(symptoms, prescription_text)
