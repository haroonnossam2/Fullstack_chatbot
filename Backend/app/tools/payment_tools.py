from langchain_core.tools import tool


@tool
def check_payment(
    customer_message: str
):
    """
    Check a demo payment issue.
    """

    message = (
        customer_message
        .lower()
    )

    if (
        "twice" in message
        or "duplicate" in message
    ):

        return {
            "issue": "duplicate charge",
            "eligible_for_review": True,
            "action": "Payment team should review duplicate transaction",
        }

    if "refund" in message:

        return {
            "issue": "refund request",
            "eligible_for_review": True,
            "action": "Refund request requires verification",
        }

    return {
        "issue": "unknown",
        "eligible_for_review": False,
        "action": "No payment issue detected",
    }