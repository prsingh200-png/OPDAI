# Architecture

Streamlit -> FastAPI -> Services -> OpenAI Responses API
                         |
                         -> SQLite
                         -> Local uploads

The API owns validation, consent checks, authentication and orchestration.
