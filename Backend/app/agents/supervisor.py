from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
import os

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


def supervisor(
    state: SupportState
):

    system_prompt = """
You are the Supervisor Agent for an
e-commerce customer support system.

Your job is to determine which specialist
should handle the customer's request.

Available specialists:

ORDER
- Order status
- Delivery status
- Order information
- Shipping questions

PAYMENT
- Payment problems
- Duplicate charges
- Refund questions
- Payment status

SUPPORT
- General questions
- Company policies
- FAQs
- Product information

Return ONLY one of:

ORDER
PAYMENT
SUPPORT
"""

    response = _get_model().invoke(
        [
            SystemMessage(
                content=system_prompt
            ),
            *state["messages"],
        ]
    )

    selected_agent = (
        response.content
        .strip()
        .upper()
    )

    if selected_agent not in {
        "ORDER",
        "PAYMENT",
        "SUPPORT",
    }:

        selected_agent = "SUPPORT"

    activity = state.get(
        "activity",
        []
    )

    activity.append(
        f"Supervisor → {selected_agent.title()} Agent"
    )

    return {
        "next_agent": selected_agent,
        "activity": activity,
    }