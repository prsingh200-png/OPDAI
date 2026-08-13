from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException, UploadFile

from app.config import get_settings
from app.utils.helpers import ensure_directory, safe_extension

async def save_upload(file: UploadFile) -> dict:
    settings = get_settings()
    extension = safe_extension(file.filename or "")
    if extension not in settings.allowed_extension_set:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: .{extension}")

    content = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail="File is too large")

    ensure_directory(settings.upload_dir)
    stored_name = f"{uuid4().hex}.{extension}"
    path = Path(settings.upload_dir) / stored_name
    path.write_bytes(content)

    return {
        "filename": file.filename,
        "stored_name": stored_name,
        "path": str(path),
        "size_bytes": len(content),
    }

def extract_text_from_upload(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return ""
    if suffix in {".txt"}:
        return Path(path).read_text(errors="ignore")
    return ""
