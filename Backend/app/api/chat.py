from fastapi import  HTTPException, APIRouter
from pydantic import BaseModel
from app.graph.workflow import graph

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

from app.database.memory import (
    get_recent_messages,
    save_message,
    delete_old_messages,
)


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

        # --------------------------------
        # 1. Load previous conversation
        # --------------------------------

        previous_messages = get_recent_messages(
            request.conversation_id,
            limit=10,
        )

        messages = []

        for message in previous_messages:

            if message["role"] == "user":

                messages.append(
                    HumanMessage(
                        content=message["content"]
                    )
                )

            elif message["role"] == "assistant":

                messages.append(
                    AIMessage(
                        content=message["content"]
                    )
                )


        # --------------------------------
        # 2. Add current user message
        # --------------------------------

        messages.append(
            HumanMessage(
                content=request.message
            )
        )


        # --------------------------------
        # 3. Save current user message
        # --------------------------------

        save_message(
            conversation_id=request.conversation_id,
            role="user",
            content=request.message,
        )


        # --------------------------------
        # 4. Run LangGraph
        # --------------------------------

        result = graph.invoke(
            {
                "messages": messages,
                "next_agent": "",
                "final_response": "",
                "last_agent": "",
                "activity": [],
            }
        )


        # --------------------------------
        # 5. Get response
        # --------------------------------

        response = result.get(
            "final_response"
        )

        if not response:
            response = (
                "Sorry, I could not process "
                "your request."
            )


        # --------------------------------
        # 6. Save assistant response
        # --------------------------------

        save_message(
            conversation_id=request.conversation_id,
            role="assistant",
            content=response,
            agent=result.get("last_agent"),
        )


        # --------------------------------
        # 7. Keep only latest 5 messages
        # --------------------------------

        delete_old_messages(
            conversation_id=request.conversation_id,
            keep=0,
        )


        return ChatResponse(
            conversation_id=request.conversation_id,
            response=response,
            agent=result.get(
                "last_agent",
                ""
            ),
            activity=result.get(
                "activity",
                []
            ),
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )