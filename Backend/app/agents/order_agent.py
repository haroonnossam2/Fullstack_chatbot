import re
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.graph.state import SupportState

from app.tools.order_tools import get_order_details


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



def order_agent(state: SupportState):

    # Find latest customer message
    customer_messages = [
        message.content
        for message in state["messages"]
        if isinstance(message, HumanMessage)
    ]

    conversation_text = "\n".join(
        customer_messages
    )

    match = re.search(
        r"\b[a-f0-9]{20,}\b",
        conversation_text,
        re.IGNORECASE,
    )

    if match:

        order_id = match.group(0)

        order_result = get_order_details.invoke(
            {
                "order_id": order_id
            }
        )

        tool_activity = (
            f"Order Agent → PostgreSQL joined lookup "
            f"for {order_id}"
        )

    else:

        order_result = {
            "status": "No order ID provided"
        }

        tool_activity = (
            "Order Agent → requested order ID"
        )

    system_prompt = f"""
You are the Order Agent for an
e-commerce customer support system.

Customer question:

{customer_messages}

PostgreSQL order information:

{order_result}

The database result may contain:

- Order status
- Purchase date
- Delivery date
- Estimated delivery date
- Customer city/state
- Products
- Product categories
- Product prices
- Freight charges
- Seller information
- Total payment amount
- Payment method
- Installments

RULES:

1. Use ONLY information returned by PostgreSQL.

2. Never invent:
   - order status
   - products
   - prices
   - payment amounts
   - seller information
   - delivery information

3. Answer only what the customer asked.

4. If the order does not exist,
   clearly tell the customer.

5. If no order ID was provided,
   ask the customer to provide their order ID.

6. Keep your response concise and helpful.

7. Do not expose raw database structures
   or JSON to the customer.
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