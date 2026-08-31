from langchain_core.tools import tool


from langchain_core.tools import tool
from sqlalchemy import text

from app.database.db import engine


@tool
def get_order_status(
    order_id: str
):
    """
    Get order status and delivery information
    from the PostgreSQL database.
    """

    query = text("""
        SELECT
            order_id,
            order_status,
            order_purchase_timestamp,
            order_delivered_carrier_date,
            order_delivered_customer_date,
            order_estimated_delivery_date
        FROM orders
        WHERE order_id = :order_id
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {
                "order_id": order_id
            }
        )

        row = result.mappings().first()

    if not row:

        return {
            "order_id": order_id,
            "status": "Order not found"
        }

    return dict(row)
