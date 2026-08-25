from langchain_core.tools import tool


DEMO_ORDERS = {

    "12345": {
        "status": "Shipped",
        "eta": "2026-08-18",
        "carrier": "Demo Express",
    },

    "67890": {
        "status": "Delivered",
        "eta": "2026-08-12",
        "carrier": "Demo Express",
    },

    "55555": {
        "status": "Processing",
        "eta": "2026-08-20",
        "carrier": "Demo Express",
    },

}


@tool
def get_order_status(
    order_id: str
):
    """
    Get the status of an order.
    """

    order = DEMO_ORDERS.get(
        order_id
    )

    if not order:

        return {
            "order_id": order_id,
            "status": "Order not found",
        }

    return {
        "order_id": order_id,
        **order,
    }