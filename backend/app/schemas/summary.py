from pydantic import BaseModel, Field

class SummaryRequest(BaseModel):
    patient_id: str
    symptoms: str = Field(min_length=2, max_length=10000)
    prescription_text: str = Field(default="", max_length=20000)

class SummaryResponse(BaseModel):
    patient_id: str
    summary: str
    requires_doctor_review: bool = True
