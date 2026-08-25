from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from langchain_core.messages import HumanMessage

from app.graph.workflow import graph


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    agent: str
    activity: list[str]


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=request.message
                    )
                ],
                "next_agent": "",
                "final_response": "",
                "last_agent": "",
                "activity": [],
            }
        )

        messages = result.get("messages", [])

        response = result.get(
            "final_response"
        )

        if not response and messages:
            response = messages[-1].content

        if not response:
            response = (
                "Sorry, I could not generate a response."
            )

        return ChatResponse(
            conversation_id=request.conversation_id,
            response=response,
            agent=result.get(
                "last_agent",
                "supervisor"
            ),
            activity=result.get(
                "activity",
                []
            ),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )