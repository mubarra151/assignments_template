### Abstract

This thesis investigates two central risks in Large Language Model (LLM) applications—prompt injection and data leakage—in practical settings such as retrieval-augmented generation (RAG) and tool-using agents. We formalize threat models for direct and indirect prompt injection and for training-time versus runtime data leakage, implement representative attacks, and evaluate layered defenses. Using established analyses of indirect prompt injection in real-world systems [1], universal jailbreak-style adversarial prompts [4], and training-data memorization and extraction [2],[3], we quantify Attack Success Rate (ASR), leakage rates, and utility trade-offs. We provide guidance for practitioners on effective mitigations, showing that layered defenses (prompt/tool hardening, sanitization, guard models, isolation, and data loss prevention) reduce risk with manageable overhead, while acknowledging limitations against adaptive attackers.

### Introduction

LLMs have rapidly transitioned from research prototypes to core components in products that retrieve external knowledge and invoke tools. This integration broadens the attack surface: adversaries can encode instructions in user inputs or untrusted documents to override system behavior (prompt injection), and can elicit model memorization or exfiltrate sensitive runtime data (data leakage). Foundational work demonstrates indirect prompt injection against deployed RAG/agent systems, leading to system prompt exposure and unsafe tool use [1]. Concurrently, studies on memorization reveal that LLMs can reproduce rare or verbatim content under certain conditions [2],[3]. Universal adversarial prompts transfer across aligned models, indicating systemic robustness challenges [4].

This thesis focuses on (i) indirect prompt injection in RAG/agent pipelines and (ii) training-time and runtime data leakage pathways. Our contributions are: (1) a taxonomy and precise threat models tailored to common LLM integration patterns; (2) an empirical study of attacks and layered defenses; (3) measurement of security–utility trade-offs; and (4) practical, reproducible defense guidance.

### Related Work

- Indirect prompt injection in real-world LLM-integrated applications shows that untrusted content can steer models, leak system prompts, and trigger tool misuse [1].
- Universal/transferable adversarial prompts and jailbreaks highlight that safety alignment remains vulnerable to carefully crafted inputs, with cross-model transfer [4].
- Training-data extraction and memorization quantify the conditions under which models emit sensitive content, impacting privacy and intellectual property [2],[3].
- Persistent deceptive behaviors and safety degradation via training processes can interact with injection/leakage risks in integrated systems [5].

### Methodology

#### Threat models
- Prompt injection: Attacker controls user inputs and/or untrusted documents/web pages consumed by RAG/agents; goals include instruction override, system prompt exposure, and unsafe tool invocation.
- Data leakage: (a) training-time memorization extraction; (b) runtime exfiltration from RAG stores, prompts, tools, or environment.
- Adversary capabilities: Black-box model access; ability to insert/host content in the RAG corpus or linked pages; no privileged tool access beyond the application interface.

#### Systems under test
- RAG pipeline: retriever + ranker + prompt constructor + generator; untrusted corpus with clean and adversarial variants.
- Tool-using agent: minimal toolset (web fetcher, sandboxed filesystem read, simple API) with JSON schemas and scoped credentials.
- Models: one open-weight model and one hosted model (where permitted) to assess cross-model effects.

#### Attacks
- Indirect prompt injection: documents with hidden instructions to exfiltrate canaries/system prompts, override tasks, or induce tool misuse [1].
- Web/HTML payloads: markup-based instructions (e.g., HTML comments/attributes/alt-text) that survive preprocessing.
- Universal jailbreak prompts: compare injection results with baseline jailbreak-style prompts [4].
- Data leakage:
  - Runtime: plant unique canary secrets in the RAG corpus and tool-accessible stores; probe with benign and adversarial prompts; measure leak rate.
  - Training-time: evaluate memorization extraction on public models using canary techniques where permitted [2],[3].

#### Defenses (evaluated singly and as layers)
- Prompt/tool hardening: least-privilege system prompts; explicit refusal and instruction-boundary templates; JSON-only function calls; parameter allowlists.
- Content pipeline: HTML/JS/CSS stripping/neutralization; instruction delimiting/quoting; source domain allowlists; per-document trust tiers; retrieval filtering; prompt-time de-injection transforms.
- Guardrails: input guards for injection; output guards for policy/secrets; DLP/redaction; canary detectors; rate limiting and review for high-risk actions.
- Isolation and provenance: sandbox tools; scoped credentials; no default network/file access; provenance logging and auditability.

#### Datasets and metrics
- Corpora: mixture of clean documents with templated adversarial content; synthetic canaries in corpus and tool stores; benign tasks for utility.
- Metrics: ASR for injection goals; canary leakage rate and tokens/time-to-leak; guard TPR/FPR; utility retention; latency and cost overhead. Report confidence intervals across 3+ seeds and diverse prompts; test robustness to paraphrasing and minor content changes.

#### Procedure and ethics
- Baseline → incrementally add defenses → ablations to quantify contributions. Log full traces; redact secrets; fix seeds; version corpora. Use only synthetic secrets; sandbox tools; comply with institutional policies.

### References (IEEE style)
[1] N. Greshake, S. Abdelnabi, M. Mishra, et al., “Not What You’ve Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection,” arXiv preprint, 2023.

[2] N. Carlini, F. Tramèr, E. Wallace, et al., “Extracting Training Data from Large Language Models,” in Proc. USENIX Security, 2021.

[3] N. Carlini, F. Tramèr, D. Song, et al., “Quantifying Memorization Across Neural Language Models,” arXiv preprint, 2022.

[4] A. Zou, Z. Wang, S. Kolter, et al., “Universal and Transferable Adversarial Attacks on Aligned Language Models,” arXiv preprint, 2023.

[5] Anthropic, “Sleeper Agents: Training Deceptive LLMs that Persist,” arXiv preprint, 2024.

