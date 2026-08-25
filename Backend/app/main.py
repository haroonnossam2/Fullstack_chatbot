try:
    from app.config import OPENAI_API_KEY  # type: ignore[import-not-found]
except ImportError:
    OPENAI_API_KEY = ""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router


app = FastAPI(
    title="Multi-Agent Customer Support API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    chat_router,
    prefix="/api")

@app.get("/")
def root():
    return {
        "message":"Multi-Agent Customer Support API"
    }

@app.get("/health")
def health():
    return {"status": "ok"}