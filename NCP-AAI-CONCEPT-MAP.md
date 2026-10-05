# NCP-AAI Concept Map: from exam questions to working code

This maps the 121 NCP-AAI practice questions to the modules where you'll **build** each
concept. The aim isn't to memorise answers. It's to have done each thing in code, so you can
explain it in an interview and use it at work.

**How to use it:** finish a module, then answer that module's questions *without* looking at the
answers, and explain *why* in one line. If you can't explain it, ask Claude before moving on.

> Note: practice-question collections often contain a few wrong or debatable answers. When the
> code you built disagrees with an answer key, trust what you can show working, and ask.

---

## ✅ Module 01: Agent loop, tools, errors, human-in-the-loop (DONE)

| Concept you built | Questions |
|---|---|
| Agent vs predefined workflow (the AI picks the steps) | Q117 |
| ReAct sequence: think → act (tool) → observe → repeat | Q66, Q42 |
| The LLM picks tools based on clear tool descriptions | Q5, Q29 |
| Tools as separate, standard-interface services (your `TOOL_FUNCTIONS` registry) | Q4 |
| Tool errors go back to the model instead of crashing (`is_error`) | Q13, Q54, Q80 |
| Retries, backoff and timeouts for unreliable APIs (*code comes in M02*) | Q10, Q77, Q112, Q43 |
| Testing resilience (fake failing tools, scripted model) | Q20 |
| **Human-in-the-loop**: approve, modify or reject before acting (your `RISKY_TOOLS`) | Q19, Q49, Q53, Q89 |

## Module 02: Tool design, structured output, resilient integrations

Your MuleSoft strength. These are integration problems.

| Concept | Questions |
|---|---|
| Schema changes break tool calls: contract tests and versioning | Q35, Q88 |
| Parsing structured vs metadata fields in API responses | Q104 |
| Evaluating tool-using agents (right tool, right arguments, success rate) | Q56, Q107 |
| Don't trust uncalibrated scores from an API blindly | Q2 |

## Module 03: Memory, context, planning, prompting

| Concept | Questions |
|---|---|
| Short-term vs long-term memory | Q14, Q31, Q57, Q72, Q118 |
| State management at scale (many conversations at once) | Q15, Q25, Q76 |
| Planning and task decomposition (multi-step, multi-day) | Q36, Q99, Q109, Q70 |
| Chain-of-Thought and its limits on small models | Q24, Q42 |
| Inconsistent outputs: prompting and sampling fixes | Q27, Q58 |
| RAG memory vs fine-tuning ("embodied" memory) | Q85, Q96, Q34 |

## Module 04: MCP and framework interoperability (MuleSoft MCP)

| Concept | Questions |
|---|---|
| Connecting agents built on different frameworks (NVIDIA Agent Intelligence / NeMo Agent Toolkit) | Q28 |
| Tools as microservices with standard interfaces (MCP is the standard) | Q4 |

## Module 05: RAG (retrieval-augmented generation)

| Concept | Questions |
|---|---|
| Chunking, embeddings, retrieval quality | Q52, Q83 |
| Reranking after retrieval | Q51, Q11 |
| RAG Fusion (multiple queries, combined rankings) | Q26, Q91 |
| Freshness and latency, vector DB as a microservice | Q33, Q121 |
| Evaluating RAG: synthetic Q&A, LLM-as-a-Judge, aggregate metrics | Q18, Q41, Q46 |
| Semantic guardrails and classifier branches in RAG | Q63, Q67 |

## Module 06: Orchestration and multi-agent systems

| Concept | Questions |
|---|---|
| Graph-based workflows with branches (LangGraph style) | Q6, Q71 |
| Multi-agent patterns: sequential, hierarchical, crews | Q3, Q16, Q21, Q64 |
| Inter-agent communication and message routing | Q115, Q94 |
| Decision transparency across agents (traces, reasoning logs) | Q17, Q39, Q60 |
| Evaluating coordination problems | Q74 |

## Module 07: Evaluation, observability, guardrails, responsible AI

| Concept | Questions |
|---|---|
| Comparing agent versions objectively (A/B, metrics, judges) | Q32, Q45, Q79, Q97 |
| Monitoring drift and declining accuracy | Q69, Q82, Q93, Q108 |
| Observability: audit trails, tracing, telemetry | Q12, Q61, Q98 |
| Optimising the wrong goal (fast but customers unhappy) | Q68, Q87, Q100 |
| Tone, clarity and user-feedback loops | Q50, Q62, Q92, Q103, Q106, Q95 |
| NeMo Guardrails: placement, coverage, LangChain integration | Q59, Q113, Q114 |
| Bias, fairness, privacy, compliance | Q8, Q84, Q86, Q111 |
| Improving agents systematically and the data flywheel (NeMo) | Q23, Q48, Q65 |

## Module 08: Deployment and scaling on the NVIDIA stack

| Concept | Questions |
|---|---|
| NIM microservices, Triton Inference Server, TensorRT-LLM | Q30, Q75, Q102, Q119 |
| Kubernetes vs Slurm, autoscaling, zero-downtime rollouts | Q7, Q9, Q22, Q38, Q44, Q105, Q110, Q116 |
| Central monitoring, CI/CD, rollbacks across regions | Q1, Q81 |
| Latency targets (<100 ms), GPU utilisation, multimodal throughput | Q37, Q55, Q90, Q101, Q120 |
| Load testing and finding bottlenecks | Q47, Q73, Q78 |
| Multimodal inputs (documents with images, dates) | Q40 |

---

**Interview tip:** for any question above, a strong answer has three parts: the concept, a
time you built it ("in my approval gate I…"), and the trade-off ("approval adds delay, so I only
apply it to risky tools").
