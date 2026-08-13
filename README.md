# OPDAI

Runnable MVP for AI-assisted OPD intake.

## 1. Setup

```bash
cd backend
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

## 2. Start backend

From `backend/`:
```bash
uvicorn app.main:app --reload --port 8000
```

Open:
http://localhost:8000/docs

## 3. Start frontend

Open a second terminal:

```bash
cd frontend
pip install streamlit requests
streamlit run streamlit_app.py
```

Open:
http://localhost:8501

## Demo doctor login

Email:
`doctor@example.com`

Password:
`ChangeMe123!`

Change these credentials in `.env` before using the application beyond local development.

## Docker

From the project root:

```bash
docker compose up --build
```

Backend:
http://localhost:8000

Frontend:
http://localhost:8501

## Important

This is an MVP and must not be used as a production clinical system without appropriate security, privacy, validation, audit controls, clinical review and regulatory assessment.
