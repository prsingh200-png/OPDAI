from fastapi import Depends, HTTPException, status
from app.auth.jwt_handler import get_current_user

def require_doctor(user=Depends(get_current_user)):
    if user.get("role") != "doctor":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctor access required")
    return user
