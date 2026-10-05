"""Test the loop without an API key by scripting a fake LLM.

This is also how professionals unit-test agents: replace the model with a scripted fake,
then check that the *loop* (tool dispatch, error handling, stopping) behaves correctly.
Run: pytest -q
"""

from types import SimpleNamespace as NS

from agent import run_agent
import tools


def text(t):
    return NS(type="text", text=t)


def tool_use(id_, name, input_):
    return NS(type="tool_use", id=id_, name=name, input=input_)


class FakeClient:
    """Returns pre-scripted responses in order and records what the agent sent."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []
        self.messages = self  # so client.messages.create(...) works

    def create(self, **kwargs):
        # Snapshot the list: the agent keeps appending to the same list object
        self.calls.append({**kwargs, "messages": list(kwargs["messages"])})
        return self.responses.pop(0)


def test_full_loop_with_tools_and_ticket(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "y")  # pretend a human typed "y"
    tools.TICKETS.clear()
    client = FakeClient([
        NS(stop_reason="tool_use", content=[tool_use("t1", "get_order", {"order_id": "ORD-1002"})]),
        NS(stop_reason="tool_use", content=[
            tool_use("t2", "convert_currency", {"amount": 89.5, "from_currency": "EUR", "to_currency": "INR"}),
            tool_use("t3", "create_support_ticket", {"order_id": "ORD-1002", "summary": "Payment failed"}),
        ]),
        NS(stop_reason="end_turn", content=[text("Payment failed. ~₹8064. Ticket TCK-001.")]),
    ])
    answer = run_agent("check ORD-1002", client, "fake", verbose=False)

    assert "TCK-001" in answer
    assert len(client.calls) == 3
    # Tool results were fed back as a user message, linked by tool_use_id
    last_msgs = client.calls[2]["messages"]
    results = last_msgs[-1]["content"]
    assert [r["tool_use_id"] for r in results] == ["t2", "t3"]
    assert '"amount": 8063.95' in results[0]["content"]


def test_tool_error_is_sent_back_to_model_not_raised():
    client = FakeClient([
        NS(stop_reason="tool_use", content=[tool_use("t1", "get_order", {"order_id": "BAD"})]),
        NS(stop_reason="end_turn", content=[text("That order ID doesn't exist.")]),
    ])
    run_agent("check BAD", client, "fake", verbose=False)
    result = client.calls[1]["messages"][-1]["content"][0]
    assert result["is_error"] is True
    assert "not found" in result["content"]


def test_max_steps_stops_infinite_loop():
    looping = NS(stop_reason="tool_use", content=[tool_use("t", "get_order", {"order_id": "ORD-1001"})])
    client = FakeClient([looping] * 20)
    assert run_agent("loop", client, "fake", verbose=False).startswith("Stopped")
