from langchain_core.tools import tool
from sqlalchemy import text

from app.database.db import engine


@tool
def get_payment_details(order_id: str):
    """
    Get payment details for an order
    together with order and product information.
    """

    query = text("""
        WITH payment_summary AS (
            SELECT
                order_id,

                SUM(payment_value) AS total_paid,

                JSON_AGG(
                    JSON_BUILD_OBJECT(
                        'payment_sequence',
                        payment_sequential,

                        'payment_type',
                        payment_type,

                        'installments',
                        payment_installments,

                        'payment_value',
                        payment_value
                    )
                    ORDER BY payment_sequential
                ) AS payments

            FROM olist_order_payments_dataset

            WHERE order_id = :order_id

            GROUP BY order_id
        ),

        item_summary AS (
            SELECT
                oi.order_id,

                JSON_AGG(
                    JSON_BUILD_OBJECT(
                        'product_id',
                        oi.product_id,

                        'category',
                        COALESCE(
                            pct.product_category_name_english,
                            p.product_category_name
                        ),

                        'price',
                        oi.price,

                        'freight_value',
                        oi.freight_value,

                        'seller',
                        s.seller_id,

                        'seller_city',
                        s.seller_city,

                        'seller_state',
                        s.seller_state
                    )
                    ORDER BY oi.order_item_id
                ) AS items

            FROM olist_order_items_dataset oi

            LEFT JOIN olist_products_dataset p
                ON oi.product_id = p.product_id

            LEFT JOIN product_category_name_translation pct
                ON p.product_category_name =
                   pct.product_category_name

            LEFT JOIN olist_sellers_dataset s
                ON oi.seller_id = s.seller_id

            WHERE oi.order_id = :order_id

            GROUP BY oi.order_id
        )

        SELECT
            o.order_id,
            o.order_status,
            o.order_purchase_timestamp,

            c.customer_id,
            c.customer_city,
            c.customer_state,

            ps.total_paid,
            ps.payments,

            i.items

        FROM olist_orders_dataset o

        LEFT JOIN olist_customers_dataset c
            ON o.customer_id = c.customer_id

        LEFT JOIN payment_summary ps
            ON o.order_id = ps.order_id

        LEFT JOIN item_summary i
            ON o.order_id = i.order_id

        WHERE o.order_id = :order_id
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