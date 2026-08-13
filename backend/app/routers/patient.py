import sqlite3
from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.schemas.patient import PatientCreate, PatientResponse
from app.utils.security import generate_id, hash_identifier

router = APIRouter(prefix="/patient", tags=["patient"])

def db():
    path = get_settings().database_url.replace("sqlite:///", "")
    return sqlite3.connect(path)

@router.post("", response_model=PatientResponse)
def create_patient(payload: PatientCreate):
    patient_id = generate_id()
    conn = db()
    conn.execute(
        "INSERT INTO patients(patient_id,name,mobile_hash,symptoms,consent_given) VALUES(?,?,?,?,0)",
        (patient_id, payload.name.strip(), hash_identifier(payload.mobile), payload.symptoms.strip()),
    )
    conn.commit()
    conn.close()
    return {
        "patient_id": patient_id,
        "name": payload.name.strip(),
        "mobile": payload.mobile,
        "symptoms": payload.symptoms.strip(),
        "consent_given": False,
    }

@router.get("/{patient_id}")
def get_patient(patient_id: str):
    conn = db()
    row = conn.execute(
        "SELECT patient_id,name,mobile_hash,symptoms,consent_given FROM patients WHERE patient_id=?",
        (patient_id,),
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "patient_id": row[0],
        "name": row[1],
        "symptoms": row[3],
        "consent_given": bool(row[4]),
    }
