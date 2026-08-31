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
Use ORDER for:
- Order status
- Where is my order
- Delivery status
- Shipping questions
- Tracking information
- Estimated delivery date

PAYMENT
Use PAYMENT for:
- Payment amount
- How much did I pay
- Payment method
- Credit card
- Payment status
- Duplicate charges
- Charges
- Refund questions
- Installments
- Billing questions

SUPPORT
Use SUPPORT for:
- General questions
- Company policies
- FAQs
- Product information
- Return policy

IMPORTANT:
If the customer asks about payment, payment
amount, payment method, credit card, charge,
refund, billing, or installments, return PAYMENT.

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