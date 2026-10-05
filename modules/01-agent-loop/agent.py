"""Module 01: an AI agent from scratch, with no framework.

The whole idea of an agent fits in one loop:

    while not done:
        response = LLM(conversation, tools)      # model reasons and picks an action
        if response wants tools:
            results = run the tools              # we act in the real world
            conversation += response + results   # model observes the results
        else:
            done = True                          # model gives the final answer

Run it:
    python agent.py "What's the status of ORD-1002 and how much is it in INR?"
"""

import json
import os
import sys

from tools import TOOL_FUNCTIONS, TOOL_SCHEMAS

SYSTEM_PROMPT = """You are an order-support agent for an e-commerce company.
Use tools to get facts. Never guess order data.
If an order has a problem, open a support ticket for it.
Keep the final answer short and include the ticket ID if you created one."""

MAX_STEPS = 8  # Safety stop, like a max-retry or timeout on a flow. Agents can loop forever.
RISKY_TOOLS = {"create_support_ticket"}  # tools that need a human "yes" first


def execute_tool(name: str, args: dict) -> tuple[str, bool]:
    """Run one tool. Returns (result_text, is_error). Errors go back to the model, not up the stack."""
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return f"Unknown tool: {name}", True
           # NEW: human approval for risky tools
    if name in RISKY_TOOLS:
        answer = input(f"\n  Agent wants to run {name}({args}). Approve? (y/n): ")
        if answer.strip().lower() != "y":
            return "A human declined this action. Do not retry. Tell the user it was not approved.", True
    try:
        return json.dumps(func(**args)), False
    except Exception as e:  # The model reads the error and can fix its next call
        return f"{type(e).__name__}: {e}", True


def run_agent(user_message: str, client, model: str, verbose: bool = True) -> str:
    messages = [{"role": "user", "content": user_message}]

    for step in range(1, MAX_STEPS + 1):
        # 1. REASON: send the whole conversation plus the tool menu to the model
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        # The model's turn (text and/or tool requests) must go into history as-is
        messages.append({"role": "assistant", "content": response.content})

        # 2. DONE? If the model didn't ask for a tool, its text is the final answer
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        # 3. ACT: run every tool the model requested in this turn
        tool_results = []
        for block in response.content:
            if block.type == "text" and block.text.strip() and verbose:
                print(f"  [step {step}] thinking: {block.text.strip()}")
            if block.type == "tool_use":
                result, is_error = execute_tool(block.name, block.input)
                if verbose:
                    flag = "ERROR " if is_error else ""
                    print(f"  [step {step}] tool {block.name}({block.input}) -> {flag}{result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,  # links the result to the specific request
                    "content": result,
                    "is_error": is_error,
                })

        # 4. OBSERVE: results go back as a *user* message, then we loop
        messages.append({"role": "user", "content": tool_results})

    return "Stopped: reached MAX_STEPS without a final answer."


if __name__ == "__main__":
    from anthropic import Anthropic
    from dotenv import load_dotenv

    load_dotenv()
    question = " ".join(sys.argv[1:]) or "Check ORD-1002. What's wrong and how much is it in INR?"
    print(f"USER: {question}\n")
    answer = run_agent(question, Anthropic(), os.getenv("MODEL", "claude-sonnet-4-5"))
    print(f"\nAGENT: {answer}")
