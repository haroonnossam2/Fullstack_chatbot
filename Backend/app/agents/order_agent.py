import re
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from app.graph.state import SupportState
from app.tools.order_tools import get_order_status


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


def order_agent(
    state: SupportState
):

    customer_message = (
        state["messages"][-1].content
    )

    match = re.search(
        r"\b\d{4,}\b",
        customer_message
    )

    if match:

        order_id = match.group(0)

        order_result = (
            get_order_status.invoke(
                {
                    "order_id": order_id
                }
            )
        )

        tool_activity = (
            f"Order Agent → "
            f"get_order_status({order_id})"
        )

    else:

        order_result = (
            "No order number was provided."
        )

        tool_activity = (
            "Order Agent → requested order number"
        )

    system_prompt = f"""
You are the Order Agent.

You handle:
- Order status
- Delivery
- Shipping
- Order information

Customer message:

{customer_message}

Order database result:

{order_result}

Rules:

1. Never invent order information.
2. If the order was not found, say so.
3. If no order number was provided,
   ask the customer for it.
4. Give a concise and helpful answer.
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