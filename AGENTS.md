# FinSight-Vertex: Agent Operating System & Workspace Protocol

Welcome to **FinSight-Vertex**, an enterprise-grade financial document lakehouse and autonomous agentic RAG system built on Google Cloud Platform (Vertex AI, BigQuery Vector Search, Document AI, Cloud Run).

This file governs the behavior, standards, multi-agent collaboration patterns, and operational protocols for all AI agents working in this repository.

---

## 1. Project Mission & Dual-Track Standard

FinSight-Vertex is engineered to demonstrate production-grade mastery across two distinct yet intersecting disciplines:

1. **Track 1: Senior Cloud Data Engineer**
   - Enterprise ETL & Document Lakehouse architecture on GCS & BigQuery.
   - High-throughput asynchronous batch processing with Google Cloud Document AI Layout Parser.
   - Table-preserving chunking with hierarchical ancestor heading context.
   - BigQuery Vector Search (`ARRAY<FLOAT64>`, IVF Cosine indexing, BQ Remote Models).
   - Strict data lineage, idempotency, and cost-optimized lakehouse design.

2. **Track 2: Autonomous GenAI / Agent Systems Engineer**
   - Multi-agent orchestration and query decomposition with Gemini 2.0 Flash.
   - Deterministic tool execution (BigQuery Vector Search, BigQuery SQL analytics, sandboxed Python math calculator).
   - High-precision grounded synthesis with mandatory page-level citations (`[Doc, Page]`).
   - Rigorous quantitative evaluation via the Vertex AI GenAI Evaluation Suite (Groundedness, Faithfulness, QA Quality).
   - Containerized production serving on Cloud Run (scale-to-zero).

Every architectural choice, line of code, and documentation artifact must reflect senior engineering rigor suitable for executive technical reviews and portfolio defense.

---

## 2. Multi-Agent Delegation & QA Architecture

To maintain high velocity while enforcing flawless engineering quality, development follows an **Agentic Delegation Model**:

```
                              ┌───────────────────────────────────────────────┐
                              │            LEAD ARCHITECT AGENT               │
                              │           (High Reasoning Model)              │
                              └──────────────────────┬────────────────────────┘
                                                     │
                         ┌───────────────────────────┴───────────────────────────┐
                         ▼                                                       ▼
           ┌───────────────────────────┐                           ┌───────────────────────────┐
           │     FAST CODER AGENTS     │                           │   MULTI-SUBAGENT QA BOARD │
           │   (flash / flash_lite)    │                           │    (Specialized Review)   │
           └─────────────┬─────────────┘                           └─────────────┬─────────────┘
                         │                                                       │
                         │ • Boilerplate & Models                                │ • Security & Sandbox Audit
                         │ • Data Transformation                                 │ • Data Integrity & Lineage
                         │ • Test Harness Generation                             │ • Code Quality & Typing
                         │ • Synthetic Q&A Sets                                  │ • Benchmark Verification
                         ▼                                                       ▼
                         └───────────────────────────┬───────────────────────────┘
                                                     ▼
                                       ┌───────────────────────────┐
                                       │     VERIFIED RELEASE      │
                                       │ (docs/ + src/ + tests/)   │
                                       └───────────────────────────┘
```

### Delegation Rules:
- **Lead Architect (High Reasoning / Parent):** Manages end-to-end orchestration, system architecture, API contracts, BigQuery schema design, evaluation methodology, and user interaction.
- **Fast Workers (`flash` / `flash_lite` subagents):** Delegated routine, high-volume, or structured implementation tasks (e.g., writing Pydantic models, JSON parsing helpers, test fixtures, synthetic benchmark queries).
- **QA & Code Review Board (Parallel Subagents):** No critical implementation is considered complete until independently evaluated by specialized subagents:
  1. **Security & Governance Reviewer:** Validates input sanitization, least-privilege IAM roles, SQL injection protection, and sandboxed Python math execution safety.
  2. **Data Integrity Reviewer:** Verifies Document AI chunk parsing fidelity, markdown table preservation, embedding dimensional alignment (768-dim), and schema consistency.
  3. **Code Quality & Reliability Reviewer:** Enforces PEP 8, strict type hints (`typing`), comprehensive docstrings, deterministic error handling, GCP client caching, and pytest coverage.

---

## 3. Mandatory Documentation & Learning Protocol

A primary objective of this project is deep foundational learning, knowledge retention, and interview readiness.

### Core Documentation Rules:
1. **Document Every Step:** All phases, architecture patterns, trade-offs, CLI recipes, and Python scripts must be documented in markdown files under `docs/phases/`.
2. **Phase Breakdown:**
   - `docs/phases/00_agentic_scaffold_and_workflow.md`: Multi-agent system, delegation protocol, and skill integration.
   - `docs/phases/01_gcp_foundation_and_storage.md`: GCS lakehouse setup, IAM least-privilege, and BigQuery datasets.
   - `docs/phases/02_sec_ingestion_and_docai.md`: SEC 10-K pipeline, Document AI Layout Parser, and table preservation.
   - `docs/phases/03_bigquery_vector_search_and_embeddings.md`: Vertex AI `text-embedding-004`, vector indexing, and BQ remote models.
   - `docs/phases/04_agentic_supervisor_and_tools.md`: Gemini 2.0 tool-calling, vector search tool, SQL tool, deterministic calculator.
   - `docs/phases/05_genai_evaluation_suite.md`: Automated evaluation benchmarks with Vertex AI GenAI Eval.
   - `docs/phases/06_streamlit_serving_and_cloud_run.md`: Streamlit dashboard, Docker containerization, Cloud Run scale-to-zero.
   - `docs/phases/07_cv_and_interview_talking_points.md`: Metrics bank, system design Q&As, and architecture trade-offs.
3. **Professional Focus:** Documentation must remain technical, professional, and career-focused. **Never mention credit consumption or promotional deadlines in learning/portfolio documentation.** Frame all cost considerations around production cloud cost optimization, serverless efficiency, and permanent Free Tier architectural design.

---

## 4. Skills & Tooling Integration

Agent skills extend capabilities across the development lifecycle. Skills are installed into `.agents/skills/`.

### Active Skills for FinSight-Vertex:
- **`bigquery-basics`**: BigQuery dataset management, table partitioning, and high-performance SQL.
- **`bigquery-ai-ml`**: BQ Remote Models, `ML.GENERATE_EMBEDDING`, and `VECTOR_SEARCH` syntax.
- **`cloud-run-basics`**: Production container deployment, resource limits, traffic management, and scale-to-zero.
- **`google-cloud-storage-basics`**: GCS bucket lifecycle, parallel transfers, and object prefix management.
- **`gcloud`**: Google Cloud CLI recipes, project configuration, and IAM role bindings.
- **`gemini-api`**: Multimodal prompting, tool-use configuration, and Vertex AI / AI Studio integration.
- **`retrieving-developer-knowledge`**: Direct access to authoritative Google Cloud technical documentation.

### Dynamic Skill Management:
When new technologies or workflows are introduced (e.g., dbt, Airflow, Terraform, LangChain, LlamaIndex), search and install the appropriate skills using:
```bash
npx skills find "<topic>"
npx skills add <owner/repo@skill> -y
```

---

## 5. Coding & Engineering Standards

- **Python Version:** Python 3.11+
- **Type Safety:** 100% type hinting using standard library `typing` and Pydantic v2 schemas.
- **Formatting & Linting:** Clean code compliant with Ruff / Black standards.
- **Testing:** Pytest unit tests for every tool and extraction module; mock external GCP services in CI.
- **Cloud Best Practices:**
  - Cache GCP clients using singleton / resource caching (`@st.cache_resource` in Streamlit).
  - Use asynchronous batch processing (`batch_process_documents`) for documents exceeding 15 pages.
  - Implement exponential backoff for all GCP API calls.
  - Never hardcode GCP project IDs, bucket names, or API keys; use environment variables or configuration files.
