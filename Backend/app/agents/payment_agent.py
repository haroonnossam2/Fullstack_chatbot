import re
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.graph.state import SupportState
from app.tools.payment_tools import (
    get_payment_details,
)

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


def payment_agent(state: SupportState):

    customer_message = next(
        (
            message.content
            for message in reversed(state["messages"])
            if isinstance(message, HumanMessage)
        ),
        ""
    )

    match = re.search(
        r"\b[a-f0-9]{20,}\b",
        customer_message,
        re.IGNORECASE
    )

    if match:

        order_id = match.group(0)

        payment_result = (
            get_payment_details.invoke(
                {
                    "order_id": order_id
                }
            )
        )

        tool_activity = (
            f"Payment Agent → PostgreSQL payment "
            f"lookup for {order_id}"
        )

    else:

        payment_result = {
            "status":
                "No order ID provided"
        }

        tool_activity = (
            "Payment Agent → requested order ID"
        )

    system_prompt = f"""
You are the Payment Agent for an
e-commerce customer support system.

Customer question:

{customer_message}

PostgreSQL payment information:

{payment_result}

The result may contain:

- Total amount paid
- Payment type
- Number of installments
- Individual payment transactions
- Order status
- Purchased products
- Product prices
- Freight amount
- Seller information

RULES:

1. Use ONLY PostgreSQL information.

2. Never invent payment information.

3. If the customer asks:

   "How much did I pay?"

   return the total_paid amount.

4. If the customer asks about
   payment method, use payment_type.

5. If the customer asks about
   installments, use installments.

6. If there are multiple payment
   transactions, explain them clearly.

7. If the order does not exist,
   clearly tell the customer.

8. If no order ID was provided,
   ask the customer for their order ID.

9. Be concise and customer friendly.

10. Do not show raw database JSON.
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
        "last_agent": "payment_agent",
        "activity": activity,
    }