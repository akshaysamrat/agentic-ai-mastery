# Module 01: The Agent Loop from Scratch

**Time:** 2 days (about 5 hrs) · **Goal:** understand exactly what an "agent" is by building one in about 80 lines, with no framework.

---

## 1. Three levels of LLM systems

| Level | What it is | MuleSoft analogy | Who controls the flow |
|---|---|---|---|
| **LLM call** | One prompt in, one answer out | A single HTTP request | Your code |
| **Workflow** | LLM calls chained in a fixed path you wrote | A flow with fixed steps | Your code |
| **Agent** | The LLM decides, step by step, which tool to call next and when to stop | A flow where the *router decides at runtime* which connector to call next, in a loop | The model |

> **Key insight:** an agent = **LLM + tools + a loop + a stop condition**. Everything else
> (memory, planning, multi-agent, MCP) is an add-on to this core.

Use the simplest level that works. Many "agent" problems are really workflows, and knowing
the difference is what interviewers test when they ask about *system design*.

## 2. The loop

```
         ┌────────────────────────────────────────────┐
         │                                            │
 user ──►│  messages ──► LLM ──► stop_reason?         │
         │     ▲                    │                 │
         │     │        "tool_use"  │  "end_turn"     │
         │     │                    ▼        └──────► final answer
         │  tool_results ◄── run tools (your code)    │
         └────────────────────────────────────────────┘
```

1. **Reason:** send the conversation and the tool list to the model.
2. **Decide:** the model replies with text, `tool_use` blocks, or both.
3. **Act:** *your code* runs the requested tools. The model never executes anything itself.
4. **Observe:** send results back as `tool_result` blocks, each linked by `tool_use_id`.
5. Repeat until `stop_reason != "tool_use"` or you hit `MAX_STEPS`.

## 3. Things that matter in production

- **The model is stateless.** Each call sends the *whole* history. Memory = what you put in
  `messages`. (Module 03 covers managing this as it grows.)
- **Tool descriptions are prompts.** Vague descriptions cause wrong tool choices. Write them like
  good API docs: what the tool does, when to use it, input format.
- **Errors are data, not exceptions.** Return a tool failure to the model with `is_error: true`
  so it can retry or change approach. This is like an On Error Continue that feeds the error back
  into the flow.
- **Always cap the loop.** `MAX_STEPS` is your timeout. Without it, a confused model can loop and burn money.
- **Parallel tool calls.** The model may request several tools in one turn. Return *all* the results
  in a single user message.
- **You are the security boundary.** The model only *requests* actions. Your code decides whether to
  run them. Later we'll add approvals for risky tools (refunds, deletes).

## 4. Read the code (in this order)

1. [`tools.py`](tools.py): tool schemas (the contract) and the functions (the implementation)
2. [`agent.py`](agent.py): the loop. Read every comment.
3. [`test_agent.py`](test_agent.py): testing an agent with a scripted fake LLM, no API key needed

```bash
cd modules/01-agent-loop
pytest -q                                   # works offline
python agent.py "Check ORD-1002. What's wrong and how much is it in INR?"   # needs API key
python agent.py "Compare the INR value of ORD-1001 and ORD-1003"
python agent.py "Check ORD-9999"            # watch it handle the error
```

Watch the `[step N]` trace. Notice when the model calls two tools in one turn, and how it
recovers from the error.

## 5. Exercises (do them, they're what make it stick)

1. **Trace by hand:** for the ORD-1002 question, write down every message in `messages`
   in order (role + content type). Then add `print(json.dumps(...))` to check your answer.
2. **Add a tool:** `get_customer_orders(customer)` returns all orders for a customer.
   Ask: "Total value of all Globex orders in USD?"
3. **Break the description:** change `get_order`'s description to `"gets stuff"`. Do the
   results change? Write down what you see in `notes/`.
4. **Approval gate:** before running `create_support_ticket`, ask `input("Approve? y/n")`.
   If refused, return an error result saying the human declined. (This is *human-in-the-loop*,
   a core pattern from Module 06.)
5. **Cost meter:** `response.usage` has `input_tokens` / `output_tokens`. Print the totals
   at the end. Notice that input tokens grow each step, because the whole history is resent.
6. **Write a test** for exercise 4 using `FakeClient`.

## 6. Interview check (answer these out loud)

- What's the difference between a workflow and an agent? When would you choose each?
- Why do tool results go back with `role: "user"`?
- What happens if a tool throws an exception, and what *should* happen?
- Why does cost grow faster than linearly with the number of steps?
- How would you stop an agent from issuing a refund without approval?

## 7. Resume line unlocked

> Built a framework-free LLM agent runtime (tool-calling loop, error recovery, step limits,
> human-approval gates) with offline unit tests using a scripted model.

**Next → Module 02: Tool design & structured output** (real APIs, Pydantic validation, retries,
idempotency: where your integration skills start to show).
