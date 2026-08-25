import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from app.graph.state import SupportState


_model = None


def _get_model() -> ChatOpenAI:
    global _model
    if _model is None:
        if not (os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_ADMIN_KEY")):
            raise RuntimeError(
                "Missing OpenAI credentials. Set OPENAI_API_KEY or OPENAI_ADMIN_KEY in the environment."
            )
        _model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
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

If a question requires access to
customer-specific data, explain what
information is required instead of
inventing information.
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