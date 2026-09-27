# Rule: Multi-Agent Delegation & Code Review Board

This rule governs the distribution of labor across agent types and enforces multi-subagent Quality Assurance (QA) before any code or pipeline artifact is accepted.

---

## 1. Principle of Reasoned Delegation

To optimize latency, cost, and cognitive efficiency:
- **Lead / Orchestrator Agent (High Reasoning):**
  - Owns system architecture, API contracts, prompt design, BigQuery schemas, and synthesis logic.
  - Formulates tasks, coordinates subagents, and synthesizes final responses.
- **Worker Subagents (Lower Reasoning - `flash` / `flash_lite`):**
  - Implement routine, well-specified code components (e.g., Pydantic schemas, data transformation functions, mock data generators).
  - Draft test cases, assertions, and synthetic benchmark Q&A pairs.
  - Perform repetitive file formatting, markdown table construction, and JSON parsing routines.

---

## 2. Multi-Subagent QA Review Board

For any code implementation, refactor, or pipeline logic, review MUST be conducted across three distinct QA dimensions using dedicated subagents:

### Dimension 1: Security & Governance Review
- **SQL Injection Prevention:** Verify all BigQuery queries use parameterized queries or strict type casting; no raw user string concatenation into SQL statements.
- **Python Sandbox Execution:** Verify that the deterministic financial calculator runs in a restricted scope (disallowing `os`, `sys`, `subprocess`, socket connections, file writes).
- **IAM & Secrets:** Ensure no service account keys, project secrets, or credentials are hardcoded. Enforce Google Application Default Credentials (ADC) and least-privilege IAM roles.

### Dimension 2: Data Integrity & Lineage Review
- **Document AI Processing:** Ensure PDF batch processing is handled asynchronously (`batch_process_documents`) for filings over 15 pages.
- **Layout & Table Preservation:** Verify that table Markdown structures are maintained without truncation and ancestor headings (`include_ancestor_headings=True`) are preserved.
- **Vector & Schema Fidelity:** Confirm embedding vectors match the required 768 dimensions for `text-embedding-004`. Verify BigQuery column types (`ARRAY<FLOAT64>`, `INT64`, `STRING`).

### Dimension 3: Code Quality, Typing & Testing
- **Type Annotations:** Enforce 100% type coverage across function arguments and return types using `typing` and Pydantic v2.
- **Error Handling & Resilience:** Validate exponential backoff retry logic for GCP API calls (`google.api_core.retry`).
- **Resource Caching:** Verify GCP clients (`bigquery.Client`, `documentai.DocumentProcessorServiceClient`) are initialized cleanly or cached via `@st.cache_resource` for Streamlit.
- **Pytest Verification:** Ensure corresponding unit tests are executed and pass before closing the task.
