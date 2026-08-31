from langchain_core.tools import tool
from sqlalchemy import text

from app.database.db import engine


@tool
def get_payment_info(
    order_id: str
):
    """
    Get payment information for an order
    from the PostgreSQL database.
    """

    query = text("""
        SELECT
            order_id,
            payment_sequential,
            payment_type,
            payment_installments,
            payment_value
        FROM order_payments
        WHERE order_id = :order_id
        ORDER BY payment_sequential
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {
                "order_id": order_id
            }
        )

        rows = result.mappings().all()

    if not rows:

        return {
            "order_id": order_id,
            "status": "Payment information not found"
        }

    return {
        "order_id": order_id,
        "payments": [
            dict(row)
            for row in rows
        ]
    }