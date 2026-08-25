# Backend

Quick start for the backend development environment.

Run the provided PowerShell helper to create a virtual environment, install requirements, and start the server:

```powershell
cd "d:\Full stack chatbot\Backend"
powershell -NoProfile -ExecutionPolicy Bypass -File .\start_backend.ps1
```

Or run manually:

```powershell
cd "d:\Full stack chatbot\Backend"
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirement.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
