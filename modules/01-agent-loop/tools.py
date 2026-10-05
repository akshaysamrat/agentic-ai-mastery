"""Tools = connectors for the LLM.

Each tool has two parts:
  1. A SCHEMA the model reads (name, description, JSON Schema input), like a RAML/OAS contract.
  2. A PYTHON FUNCTION we run when the model asks for it.

The model never runs code. It only *asks* us to run a tool, and we decide whether to.
The data below is fake so the module works offline; Module 02 swaps in real APIs.
"""

ORDERS = {
    "ORD-1001": {"status": "shipped", "amount": 120.0, "currency": "USD", "customer": "Acme Corp"},
    "ORD-1002": {"status": "payment_failed", "amount": 89.5, "currency": "EUR", "customer": "Globex"},
    "ORD-1003": {"status": "processing", "amount": 15000.0, "currency": "INR", "customer": "Initech"},
}

FX_TO_INR = {"USD": 83.2, "EUR": 90.1, "INR": 1.0}

TICKETS: list[dict] = []


def get_order(order_id: str) -> dict:
    if order_id not in ORDERS:
        # Raise a clear error. The agent loop sends it back to the model, which can recover.
        raise KeyError(f"Order {order_id} not found. Valid format is ORD-XXXX.")
    return {"order_id": order_id, **ORDERS[order_id]}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    f, t = from_currency.upper(), to_currency.upper()
    if f not in FX_TO_INR or t not in FX_TO_INR:
        raise ValueError(f"Unsupported currency. Supported: {sorted(FX_TO_INR)}")
    converted = amount * FX_TO_INR[f] / FX_TO_INR[t]
    return {"amount": round(converted, 2), "currency": t}


def create_support_ticket(order_id: str, summary: str, priority: str = "medium") -> dict:
    ticket = {"ticket_id": f"TCK-{len(TICKETS) + 1:03d}", "order_id": order_id,
              "summary": summary, "priority": priority}
    TICKETS.append(ticket)
    return ticket


# The registry: tool name -> python function. Like a connector config lookup.
TOOL_FUNCTIONS = {
    "get_order": get_order,
    "convert_currency": convert_currency,
    "create_support_ticket": create_support_ticket,
}

# What the model sees. The descriptions matter a lot: they are prompts for tool choice.
TOOL_SCHEMAS = [
    {
        "name": "get_order",
        "description": "Look up one order by ID. Returns status, amount, currency and customer. "
                       "Use this before answering any question about a specific order.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string", "description": "Order ID like ORD-1001"}},
            "required": ["order_id"],
        },
    },
    {
        "name": "convert_currency",
        "description": "Convert an amount between USD, EUR and INR using today's internal rate.",
        "input_schema": {
            "type": "object",
            "properties": {
                "amount": {"type": "number"},
                "from_currency": {"type": "string", "enum": ["USD", "EUR", "INR"]},
                "to_currency": {"type": "string", "enum": ["USD", "EUR", "INR"]},
            },
            "required": ["amount", "from_currency", "to_currency"],
        },
    },
    {
        "name": "create_support_ticket",
        "description": "Open a support ticket for an order that has a problem (for example, "
                       "payment_failed). Only create a ticket when the order has an actual issue.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "summary": {"type": "string", "description": "One-sentence description of the issue"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"]},
            },
            "required": ["order_id", "summary"],
        },
    },
]
