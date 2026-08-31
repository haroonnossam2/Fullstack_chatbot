import re
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.graph.state import SupportState
from app.tools.payment_tools import get_payment_info


_model = None


def _get_model() -> ChatOpenAI:

    global _model

    if _model is None:

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "Missing OPENAI_API_KEY in environment."
            )

        _model = ChatOpenAI(
            model="gpt-5.4-mini",
            temperature=50,
            api_key=api_key,
        )

    return _model


def payment_agent(
    state: SupportState
):

    # Get latest user message
    customer_message = next(
        (
            message.content
            for message in reversed(state["messages"])
            if isinstance(message, HumanMessage)
        ),
        ""
    )

    # Extract Olist order ID
    match = re.search(
        r"\b[a-f0-9]{20,}\b",
        customer_message,
        re.IGNORECASE
    )

    if match:

        order_id = match.group(0)

        payment_result = get_payment_info.invoke(
            {
                "order_id": order_id
            }
        )

        tool_activity = (
            f"Payment Agent → "
            f"PostgreSQL payment lookup for {order_id}"
        )

    else:

        payment_result = {
            "status": "No order ID provided"
        }

        tool_activity = (
            "Payment Agent → requested order ID"
        )

    system_prompt = f"""
You are the Payment Agent for an e-commerce
customer support system.

Customer message:

{customer_message}

Payment database result:

{payment_result}

Rules:

1. Use ONLY the payment database result for
   payment-specific information.

2. Never invent payment information.

3. If payment information was not found,
   clearly say so.

4. If no order ID was provided, ask the
   customer to provide the order ID.

5. Give a concise and helpful answer.
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

    activity.append(tool_activity)

    return {
        "messages": [response],
        "final_response": response.content,
        "last_agent": "payment_agent",
        "activity": activity,
    }