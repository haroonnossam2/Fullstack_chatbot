import re
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.graph.state import SupportState
from app.tools.order_tools import get_order_status


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


def order_agent(
    state: SupportState
):

    # Get the latest HumanMessage
    customer_message = next(
        (
            message.content
            for message in reversed(state["messages"])
            if isinstance(message, HumanMessage)
        ),
        ""
    )

    # Find Olist order ID
    match = re.search(
        r"\b[a-f0-9]{20,}\b",
        customer_message,
        re.IGNORECASE
    )

    if match:

        order_id = match.group(0)

        # Call PostgreSQL tool
        order_result = get_order_status.invoke(
            {
                "order_id": order_id
            }
        )

        tool_activity = (
            f"Order Agent → "
            f"PostgreSQL lookup for {order_id}"
        )

    else:

        order_result = {
            "status": "No order number provided"
        }

        tool_activity = (
            "Order Agent → requested order ID"
        )

    system_prompt = f"""
You are the Order Agent for an e-commerce
customer support system.

Customer message:

{customer_message}

Order database result:

{order_result}

Rules:

1. Use ONLY the order database result for
   order-specific information.

2. Never invent order information.

3. If the order was not found, clearly say so.

4. If no order ID was provided, ask the
   customer to provide their order ID.

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

    activity.append(
        tool_activity
    )

    return {
        "messages": [response],
        "final_response": response.content,
        "last_agent": "order_agent",
        "activity": activity,
    }