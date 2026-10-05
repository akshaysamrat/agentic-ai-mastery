"""Module 01, FREE version: the same agent loop, using a free API (NVIDIA or Google Gemini).

Same idea as agent.py, but in the "OpenAI-compatible" format. Most providers (Gemini,
Groq, OpenRouter, Ollama on your own PC) accept this format, so learning it pays off twice.

Setup (free): use NVIDIA (build.nvidia.com) or Google Gemini. Pick one with PROVIDER in .env.
  NVIDIA key: build.nvidia.com -> any model -> "Get API Key"   Gemini key: aistudio.google.com/apikey
  Then copy .env.example to .env and paste your key.
Run:
  python agent_free.py "Check ORD-1002. What's wrong and how much is it in INR?"
"""

import json
import os
import sys

from agent import MAX_STEPS, SYSTEM_PROMPT, execute_tool
from tools import TOOL_SCHEMAS

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Same tools, wrapped in the OpenAI format: {"type": "function", "function": {...}}
OPENAI_TOOLS = [
    {"type": "function", "function": {
        "name": t["name"], "description": t["description"], "parameters": t["input_schema"]}}
    for t in TOOL_SCHEMAS
]


def run_agent(user_message: str, client, model: str, verbose: bool = True) -> str:
    # In this format, the system prompt is just the first message
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for step in range(1, MAX_STEPS + 1):
        # 1. REASON: send the conversation plus the tool menu
        response = client.chat.completions.create(model=model, messages=messages, tools=OPENAI_TOOLS)
        msg = response.choices[0].message

        # 2. DONE? No tool calls means this is the final answer
        if not msg.tool_calls:
            return msg.content or ""

        # Save the model's turn (including its tool requests) in the history
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [{"id": c.id, "type": "function",
                            "function": {"name": c.function.name, "arguments": c.function.arguments}}
                           for c in msg.tool_calls],
        })

        # 3. ACT: run each requested tool (arguments arrive as a JSON *string*)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            result, is_error = execute_tool(call.function.name, args)
            if verbose:
                flag = "ERROR " if is_error else ""
                print(f"  [step {step}] tool {call.function.name}({args}) -> {flag}{result}")
            # 4. OBSERVE: each result is its own "tool" message, linked by tool_call_id
            messages.append({"role": "tool", "tool_call_id": call.id,
                             "content": ("ERROR: " if is_error else "") + result})

    return "Stopped: reached MAX_STEPS without a final answer."


# Same code, different provider: only the URL, key and model name change.
PROVIDERS = {
    "nvidia": ("https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY", "NVIDIA_MODEL",
               "nvidia/nemotron-3-super-120b-a12b"),
    "gemini": (GEMINI_BASE_URL, "GEMINI_API_KEY", "GEMINI_MODEL", "gemini-2.5-flash"),
}

if __name__ == "__main__":
    from dotenv import load_dotenv
    from openai import OpenAI

    # Load the .env file from the repo root (two folders up from this file)
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
    load_dotenv(env_path)
    provider = os.getenv("PROVIDER", "nvidia").strip().lower()
    base_url, key_var, model_var, default_model = PROVIDERS[provider]
    api_key = os.getenv(key_var, "").strip()
    if not api_key or "paste" in api_key:
        sys.exit(f"No API key found. Open the .env file in the repo root and set {key_var}=your-key, "
                 f"then save with Ctrl+S.\n(Looked in: {os.path.abspath(env_path)})")
    client = OpenAI(api_key=api_key, base_url=base_url)
    model = os.getenv(model_var, default_model)

    question = " ".join(sys.argv[1:]) or "Check ORD-1002. What's wrong and how much is it in INR?"
    print(f"[{provider} / {model}]\nUSER: {question}\n")
    print(f"\nAGENT: {run_agent(question, client, model)}")
