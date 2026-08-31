# Backend

This folder contains the FastAPI + LangGraph backend for the Full Stack Chatbot.

## Backend Overview

The backend exposes a REST API for the chatbot and orchestrates a multi-agent workflow using LangGraph.

### Main responsibilities

- receive chat requests from the React frontend
- route customer questions to the right specialist agent
- call domain-specific tools for order and payment logic
- return the final answer and activity trail to the frontend

## Project Structure

```text
Backend/
├── app/
│   ├── agents/
│   │   ├── order_agent.py
│   │   ├── payment_agent.py
│   │   ├── supervisor.py
│   │   └── support_agent.py
│   ├── api/
│   │   └── chat.py
│   ├── graph/
│   │   ├── state.py
│   │   └── workflow.py
│   ├── tools/
│   │   ├── order_tools.py
│   │   └── payment_tools.py
│   ├── __init__.py
│   └── main.py
├── requirement.txt
├── start_backend.ps1
└── README.md
```

## Run the backend

### Option 1: Use the PowerShell helper

```powershell
cd "d:\Full stack chatbot\Backend"
powershell -NoProfile -ExecutionPolicy Bypass -File .\start_backend.ps1
```

### Option 2: Run manually

```powershell
cd "d:\Full stack chatbot\Backend"
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirement.txt
$env:OPENAI_API_KEY = "your_api_key_here"
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## API endpoint

```http
POST /api/chat
```

Example request body:

```json
{
  "message": "I was charged twice",
  "conversation_id": "demo"
}
```

Example response:

```json
{
  "conversation_id": "demo",
  "response": "I can help look into the duplicate charge...",
  "agent": "payment_agent",
  "activity": [
    "Supervisor → Payment Agent",
    "Payment Agent → check_payment()"
  ]
}
```

## Workflow summary

The backend graph follows this route:

```text
START -> supervisor -> ORDER/PAYMENT/SUPPORT -> END
```

- `supervisor` decides which agent handles the request.
- `order_agent` handles order lookup and shipping questions.
- `payment_agent` handles payment issues and refund questions.
- `support_agent` handles general support and FAQ requests.

## Environment variable

```powershell
$env:OPENAI_API_KEY = "your_openai_key"
```

This is required for the LLM calls used by the supervisor and specialist agents.

## Notes

The system uses demo tools and sample data for orders and payments, so it is a good starting point for a production-ready customer support workflow.

