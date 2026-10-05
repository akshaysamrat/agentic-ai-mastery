# Agentic AI Mastery: Integration Developer → Agentic AI Engineer

A 6-week, build-first path (2–3 hrs/day) from MuleSoft integration developer to
**agentic AI system designer and developer**. Every module ends in working code.
Every project is built to work both as a **portfolio piece** and as a **product
you could sell** (the `agent-store-AI` idea).

## Why your background is an advantage

An agent is mostly an **integration problem**: an LLM decides which systems to call,
and the hard engineering is in the calls themselves (auth, schemas, retries,
idempotency, rate limits, error handling, observability). You already do this every day.

| MuleSoft concept            | Agentic AI equivalent                              |
|-----------------------------|----------------------------------------------------|
| Flow / orchestration        | Agent loop / workflow graph                        |
| Connector                   | Tool (function the LLM can call)                   |
| RAML / OAS spec             | Tool schema (JSON Schema)                          |
| Anypoint Exchange           | MCP server registry / agent tool marketplace       |
| DataWeave transform         | Structured output + validation                     |
| Choice router               | LLM router / classifier step                       |
| Scatter-Gather              | Parallel sub-agents (fan-out / fan-in)             |
| Error handler / retry       | Tool error feedback to the model, retries, fallbacks |
| Object Store / VM queue     | Agent memory / durable state / checkpoints         |
| API Manager policies        | Guardrails, auth, rate & cost limits               |
| Anypoint Monitoring         | Tracing + evals (LLM observability)                |

**Your positioning:** *"Integration engineer who builds production agents: I connect
LLMs to real enterprise systems safely."* That niche is in demand and less crowded
than "I built a chatbot".

## Roadmap

| Week | Modules (learn)                                                       | Project (build → resume + sell) |
|------|-----------------------------------------------------------------------|---------------------------------|
| 1    | **01 Agent loop from scratch** · 02 Tool design & structured output · 03 Memory & context engineering | Small CLI agent over real APIs |
| 2    | 04 MCP: Model Context Protocol (servers, clients, transports, auth)    | **P1: OpenAPI → MCP Server Generator** (turn any API spec into tools any agent can use) |
| 3    | 05 RAG & retrieval agents (chunking, embeddings, hybrid search, reranking) | **P2: Integration Ops Copilot** (answers from runbooks, reads logs, triages incidents) |
| 4    | 06 Orchestration patterns: router, orchestrator-workers, evaluator-optimizer, multi-agent, human-in-the-loop, durable state | **P3: Order-to-Cash Agent** (multi-step business process with approvals) |
| 5    | 07 Production: evals, tracing, guardrails, prompt-injection defense, cost/latency | Harden P3: eval suite, dashboard, CI |
| 6    | 08 Deploy & sell: FastAPI, Docker, cloud, packaging, pricing, listing in MCP registries | Resume, portfolio site, launch P1 |

**Alongside the modules:**
- **Python track** (30–45 min/day): only the Python each module needs, with MuleSoft comparisons.
- **NCP-AAI concept map**: all 121 NVIDIA certification practice questions mapped to the module
  where you build that concept, in [`NCP-AAI-CONCEPT-MAP.md`](NCP-AAI-CONCEPT-MAP.md).
- **Free LLMs:** NVIDIA build.nvidia.com (Nemotron) by default, Gemini as backup.
- **NVIDIA stack:** NeMo Agent Toolkit (M06), NeMo Guardrails (M07), NIM/Triton (M08).

Progress is tracked in [`PROGRESS.md`](PROGRESS.md).

## Repo layout

```
modules/   one folder per module: LESSON.md + runnable code + exercises
projects/  portfolio projects (each becomes its own repo later)
resume/    resume drafts, updated as projects ship
notes/     your own notes and interview Q&A
```

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then put your API key in .env
```

Start here: [`modules/01-agent-loop/LESSON.md`](modules/01-agent-loop/LESSON.md)
