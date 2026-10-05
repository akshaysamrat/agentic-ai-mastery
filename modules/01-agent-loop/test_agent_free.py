"""Offline test for the free (OpenAI-format) agent, using a scripted fake model."""

from types import SimpleNamespace as NS

import tools
from agent_free import run_agent


def call(id_, name, args):
    return NS(id=id_, function=NS(name=name, arguments=args))


def reply(tool_calls=None, content=None):
    return NS(choices=[NS(message=NS(tool_calls=tool_calls, content=content))])


class FakeClient:
    def __init__(self, responses):
        self.responses, self.calls = list(responses), []
        self.chat = NS(completions=self)

    def create(self, **kwargs):
        self.calls.append(list(kwargs["messages"]))
        return self.responses.pop(0)


def test_free_agent_loop():
    tools.TICKETS.clear()
    client = FakeClient([
        reply([call("c1", "get_order", '{"order_id": "ORD-1002"}')]),
        reply([call("c2", "create_support_ticket", '{"order_id": "ORD-1002", "summary": "Payment failed"}')]),
        reply(content="Payment failed. Ticket TCK-001."),
    ])
    assert "TCK-001" in run_agent("check ORD-1002", client, "fake", verbose=False)
    last = client.calls[2][-1]
    assert last["role"] == "tool" and last["tool_call_id"] == "c2"
