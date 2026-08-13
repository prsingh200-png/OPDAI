import sqlite3
from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth import require_doctor
from app.config import get_settings
from app.schemas.summary import SummaryRequest, SummaryResponse
from app.services.summary_service import create_summary

router = APIRouter(prefix="/summary", tags=["summary"])

@router.post("", response_model=SummaryResponse)
def make_summary(payload: SummaryRequest, doctor=Depends(require_doctor)):
    path = get_settings().database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(path)
    patient = conn.execute(
        "SELECT patient_id, consent_given FROM patients WHERE patient_id=?",
        (payload.patient_id,),
    ).fetchone()
    upload = conn.execute(
        "SELECT path FROM uploads WHERE patient_id=? ORDER BY id DESC LIMIT 1",
        (payload.patient_id,),
    ).fetchone()
    conn.close()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not patient[1]:
        raise HTTPException(status_code=400, detail="Patient consent is required")

    summary = create_summary(payload.symptoms, upload[0] if upload else None)

    conn = sqlite3.connect(path)
    conn.execute(
        "INSERT INTO summaries(patient_id,summary,created_by) VALUES(?,?,?)",
        (payload.patient_id, summary, doctor["sub"]),
    )
    conn.commit()
    conn.close()

    return {"patient_id": payload.patient_id, "summary": summary, "requires_doctor_review": True}

@router.get("/{patient_id}")
def get_summaries(patient_id: str, doctor=Depends(require_doctor)):
    path = get_settings().database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(path)
    rows = conn.execute(
        "SELECT id,summary,created_at FROM summaries WHERE patient_id=? ORDER BY id DESC",
        (patient_id,),
    ).fetchall()
    conn.close()
    return [{"id": r[0], "summary": r[1], "created_at": r[2]} for r in rows]
