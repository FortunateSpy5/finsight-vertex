# Rule: Python Quality, Sandboxing & Testing Standards

This rule specifies Python coding conventions, typing requirements, security sandbox constraints, and automated testing standards.

---

## 1. Pythonic Architecture & Typing

- **Python Version:** 3.11+
- **Type Annotations:** Full type hinting (`typing.Optional`, `typing.List`, `typing.Dict`, `typing.Union`, `typing.Callable`).
- **Data Modeling:** Use Pydantic v2 `BaseModel` for structured payloads (e.g., chunk schemas, evaluation sets, API response structures).
- **Environment Management:** Avoid hardcoded secrets. Use environment variables with sensible defaults or Google Cloud Application Default Credentials (ADC).

---

## 2. Deterministic Financial Math & Sandboxing

FinSight-Vertex uses deterministic Python calculation tools to eliminate LLM arithmetic hallucinations.

### Sandboxing Requirements:
- Execute mathematical calculations using Python `exec()` or `eval()` inside an isolated namespace.
- **Allowed Globals:** Only `math`, `numpy`, and basic arithmetic primitives (`abs`, `round`, `sum`, `min`, `max`, `len`, `int`, `float`).
- **Strictly Prohibited:** `import os`, `import sys`, `import subprocess`, `import socket`, `open()`, filesystem access, network access, or arbitrary module execution.
- Any attempt to access restricted builtins must raise a `SecurityException` and log the event.

---

## 3. Automated Testing with Pytest

- **Unit Test Coverage:** All core modules under `src/` must have corresponding test suites in `tests/`:
  - `tests/test_docai_parser.py`: Chunk extraction, header lineage, and table structure validation.
  - `tests/test_embedder.py`: Batching logic, embedding dimensions (768), error retries.
  - `tests/test_bq_loader.py`: JSONL generation and schema compliance.
  - `tests/test_supervisor.py`: Query routing and tool call dispatching.
  - `tests/test_math_tool.py`: Deterministic arithmetic, financial ratio accuracy, and sandbox isolation defense.
- **Mocking:** Mock all external GCP network calls (Document AI, BigQuery, Vertex AI) using `unittest.mock` to ensure fast, isolated offline CI runs.
