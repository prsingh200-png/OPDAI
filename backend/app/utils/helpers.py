from pathlib import Path

def ensure_directory(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def safe_extension(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")
