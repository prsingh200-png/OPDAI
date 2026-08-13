import sqlite3
from fastapi import APIRouter, File, UploadFile, HTTPException

from app.config import get_settings
from app.services.upload_service import save_upload

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/prescription")
async def upload_prescription(patient_id: str, file: UploadFile = File(...)):
    path = get_settings().database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(path)
    exists = conn.execute("SELECT 1 FROM patients WHERE patient_id=?", (patient_id,)).fetchone()
    conn.close()
    if not exists:
        raise HTTPException(status_code=404, detail="Patient not found")

    result = await save_upload(file)

    conn = sqlite3.connect(path)
    conn.execute(
        "INSERT INTO uploads(patient_id,original_name,stored_name,path) VALUES(?,?,?,?)",
        (patient_id, result["filename"], result["stored_name"], result["path"]),
    )
    conn.commit()
    conn.close()

    return {"patient_id": patient_id, **result}
