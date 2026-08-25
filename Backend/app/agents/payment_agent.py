import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from app.graph.state import SupportState
from app.tools.payment_tools import check_payment


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


def payment_agent(
    state: SupportState
):

    customer_message = (
        state["messages"][-1].content
    )

    payment_result = (
        check_payment.invoke(
            {
                "customer_message":
                customer_message
            }
        )
    )

    system_prompt = f"""
You are the Payment Agent.

You handle:

- Payments
- Duplicate charges
- Refunds
- Payment status

Customer message:

{customer_message}

Payment system result:

{payment_result}

Rules:

1. Never claim a refund was actually issued.
2. Explain what the payment system found.
3. Explain the next step.
4. Be concise.
"""

    response = _get_model().invoke(
        [
            SystemMessage(
                content=system_prompt
            )
        ]
    )

    activity = state.get(
        "activity",
        []
    )

    activity.append(
        "Payment Agent → check_payment()"
    )

    return {
        "messages": [response],
        "final_response": response.content,
        "last_agent": "payment_agent",
        "activity": activity,
    }