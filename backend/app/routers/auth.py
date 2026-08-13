from fastapi import APIRouter, HTTPException
from app.config import get_settings
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    settings = get_settings()
    if payload.email != settings.doctor_email or payload.password != settings.doctor_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(payload.email, "doctor")
    return {"access_token": token, "token_type": "bearer", "role": "doctor"}
