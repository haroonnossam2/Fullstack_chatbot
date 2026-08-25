from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.graph.state import SupportState

from app.agents.supervisor import (
    supervisor
)

from app.agents.order_agent import (
    order_agent
)

from app.agents.payment_agent import (
    payment_agent
)

from app.agents.support_agent import (
    support_agent
)


def route_agent(
    state: SupportState
):

    return state["next_agent"]


builder = StateGraph(
    SupportState
)


# -----------------------------
# Nodes
# -----------------------------

builder.add_node(
    "supervisor",
    supervisor
)

builder.add_node(
    "order",
    order_agent
)

builder.add_node(
    "payment",
    payment_agent
)

builder.add_node(
    "support",
    support_agent
)


# -----------------------------
# START
# -----------------------------

builder.add_edge(
    START,
    "supervisor"
)


# -----------------------------
# Supervisor routing
# -----------------------------

builder.add_conditional_edges(

    "supervisor",

    route_agent,

    {
        "ORDER": "order",
        "PAYMENT": "payment",
        "SUPPORT": "support",
    }

)


# -----------------------------
# END
# -----------------------------

builder.add_edge(
    "order",
    END
)

builder.add_edge(
    "payment",
    END
)

builder.add_edge(
    "support",
    END
)


graph = builder.compile()