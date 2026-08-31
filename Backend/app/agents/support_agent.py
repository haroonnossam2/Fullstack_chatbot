import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from app.graph.state import SupportState


_model = None


def _get_model() -> ChatOpenAI:
    global _model

    if _model is None:

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "Missing OPENAI_API_KEY in the environment."
            )

        _model = ChatOpenAI(
            model="gpt-5.4-mini",
            temperature=50,
            api_key=api_key,
        )

    return _model


def support_agent(
    state: SupportState
):

    system_prompt = """
You are the General Support Agent.

Handle:
- General questions
- FAQs
- Product questions
- Company policies
- Return policy questions

Be helpful and concise.

If a question requires customer-specific data,
explain what information is required instead
of inventing information.
"""

    response = _get_model().invoke(
        [
            SystemMessage(
                content=system_prompt
            ),
            *state["messages"],
        ]
    )

    activity = state.get(
        "activity",
        []
    )

    activity.append(
        "Support Agent → Knowledge Base"
    )

    return {
        "messages": [response],
        "final_response": response.content,
        "last_agent": "support_agent",
        "activity": activity,
    }