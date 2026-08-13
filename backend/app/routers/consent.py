import sqlite3
from datetime import datetime, timezone
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.config import get_settings

router = APIRouter(prefix="/consent", tags=["consent"])

class ConsentRequest(BaseModel):
    patient_id: str
    consent_given: bool

@router.post("")
def set_consent(payload: ConsentRequest):
    if not payload.consent_given:
        raise HTTPException(status_code=400, detail="Consent is required for this MVP flow")
    path = get_settings().database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(path)
    cur = conn.execute(
        "UPDATE patients SET consent_given=1, consent_at=? WHERE patient_id=?",
        (datetime.now(timezone.utc).isoformat(), payload.patient_id),
    )
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"patient_id": payload.patient_id, "consent_given": True}
