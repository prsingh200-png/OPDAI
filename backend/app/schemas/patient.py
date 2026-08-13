from pydantic import BaseModel, Field

class PatientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    mobile: str = Field(min_length=10, max_length=20)
    symptoms: str = Field(min_length=2, max_length=5000)

class PatientResponse(BaseModel):
    patient_id: str
    name: str
    mobile: str
    symptoms: str
    consent_given: bool
