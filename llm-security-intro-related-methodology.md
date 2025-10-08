### Introduction

Large Language Models (LLMs) enable natural-language interfaces, retrieval-augmented generation (RAG), and tool-using agents, but they also introduce new risks centered on prompt injection and data leakage. Prompt injection turns instructions into an attack surface: hidden or adversarial directives embedded in user input or untrusted documents/web pages can steer model behavior, leak system prompts, or trigger unsafe tool actions [1],[4]. Data leakage manifests both as exposure of sensitive training data due to memorization [2],[3] and as exfiltration of private runtime data (e.g., documents in a vector store, credentials, or files/tools accessible to an agent) via indirect prompt injection [1] and weak isolation.

This work focuses on these two risks in practical LLM applications. We (1) formalize threat models for direct and indirect prompt injection and for training-time versus runtime data leakage; (2) empirically evaluate representative attacks against RAG pipelines and tool-using agents; (3) measure the effectiveness and cost of defenses (prompt/tool hardening, sanitization, guard models, isolation, DLP/redaction, provenance); and (4) provide actionable guidance with quantified security–utility trade-offs.

### Related Work

- Prompt injection in RAG/agents: Foundational analyses show untrusted content can override system instructions, exfiltrate secrets, and induce unsafe tool use in real applications [1]. Follow-on work demonstrates universal/transferable jailbreak-style attacks on aligned models [4] and highlights multi-turn escalation as well as markup/HTML/CSS-based payloads that survive naive sanitization. Industry guidance (OWASP LLM Top 10) elevates prompt injection and data exfiltration as primary risks for LLM apps [5].

- Data leakage and memorization: Studies demonstrate extraction of rare or verbatim sequences from LLMs and quantify conditions that increase leakage (model size, duplication, temperature) [2],[3]. Runtime leakage in RAG/agents includes canary exfiltration from vector stores and credentials/secrets disclosure via tool calls or system prompt extraction [1]. Separate lines of work explore safety-degrading/backdoor behaviors that may interact with injection/leakage risks in integrated systems [6].

- Defenses: Proposed mitigations include least-privilege system prompts and explicit refusal policies; content sanitization and domain allowlists; LLM-based input/output guards (safety/PII/DLP); canary tokens and leakage detection; and architectural isolation for tools and credentials [5]. Practical evaluations often find that layered controls are necessary and that adaptive attacks reduce single-defense effectiveness.

### Methodology

#### Threat models
- Prompt injection: Adversary controls user input and/or untrusted documents/web pages consumed by RAG/agents; goals include instruction override, system prompt exposure, and unsafe tool invocation.
- Data leakage: (a) training-time memorization (attacker queries to extract secrets); (b) runtime exfiltration from RAG stores, prompts, tools, or environment (attacker uses indirect injection and elicitation to retrieve canaries/secrets).
- Adversary capabilities: Black-box access to model; ability to insert/host content in the RAG corpus or linked pages; no privileged access to tools beyond what the application exposes.

#### Systems under test
- RAG pipeline: retriever + ranker + prompt constructor + generator, with an untrusted corpus (clean vs adversarial variants).
- Tool-using agent: minimal tool set (e.g., web fetcher, filesystem read of a sandboxed directory, simple API) with explicit JSON schemas and scoped credentials.
- Models: at least one open model and one hosted model (where permitted) to assess cross-model effects.

#### Attacks
- Indirect prompt injection (RAG): adversarial documents with hidden instructions to (i) exfiltrate canaries/system prompts; (ii) override task; (iii) induce tool misuse.
- Web/HTML payloads: markup-based instructions, comments/alt-text prompts that persist through preprocessing.
- Direct jailbreak baselines: to compare injection vs. jailbreak success under the same safety policies [4].
- Data leakage
  - Runtime: plant unique canary secrets in the RAG corpus and tool-accessible stores; query with benign and adversarial prompts; measure leak rate.
  - Training-time: evaluate memorization extraction on public models using known canary techniques where permitted [2],[3].

#### Defenses (evaluated singly and in combinations)
- Prompt/tool hardening: least-privilege system prompts; explicit “ignore external instructions” templates; JSON-only function calls; parameter allowlists.
- Content pipeline: HTML/JS/CSS stripping/neutralization; instruction delimiting/quoting; source domain allowlists; per-document trust tiers; retrieval filtering; prompt-time de-injection transforms.
- Guardrails: input guard for suspected injection; output guard for policy/secrets; DLP/redaction; canary detectors; rate limiting and review for high-risk actions.
- Isolation and provenance: sandbox tools; scoped credentials; no default network/file access; provenance logging and auditability.

#### Datasets and metrics
- Adversarial doc set (hand-crafted + templated) mixed into a clean corpus; synthetic canaries in corpus and tool stores; benign task set for utility.
- Primary: Attack Success Rate (ASR) for injection goals (override, prompt exposure, tool misuse); canary leakage rate; tokens/time-to-leak.
- Secondary: guard true/false positive rates; utility retention on benign tasks; latency and cost overhead.
- Report confidence intervals across 3+ seeds and diverse prompt templates; test robustness to paraphrasing and minor content changes.

#### Procedure and ethics
- Baseline → add defenses incrementally → ablations to quantify contributions. Log full traces; redact secrets; fix seeds; version corpora.
- Use only synthetic harmful tasks and secrets; sandbox tools; adhere to platform/institutional policies.

### References (IEEE style)
[1] N. Greshake, S. Abdelnabi, M. Mishra, et al., “Not What You’ve Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection,” arXiv preprint, 2023.

[2] N. Carlini, F. Tramèr, E. Wallace, et al., “Extracting Training Data from Large Language Models,” in Proc. USENIX Security, 2021.

[3] N. Carlini, F. Tramer, D. Song, et al., “Quantifying Memorization Across Neural Language Models,” arXiv preprint, 2022.

[4] A. Zou, Z. Wang, S. Kolter, et al., “Universal and Transferable Adversarial Attacks on Aligned Language Models,” arXiv preprint, 2023.

[5] OWASP, “Top 10 for Large Language Model Applications,” Project guidance, 2023–2024.

[6] Anthropic, “Sleeper Agents: Training Deceptive LLMs that Persist,” arXiv preprint, 2024.

