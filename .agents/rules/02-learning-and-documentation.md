# Rule: Documentation & Professional Learning Standards

This rule establishes the framework for documenting every milestone, architectural decision, and implementation step in `FinSight-Vertex`.

---

## 1. Core Principle: Documentation as a Learning & CV Asset

The primary goal of this repository is personal technical growth, mastery of modern cloud data engineering and autonomous AI agent architectures, and building verifiable portfolio proof for senior engineering roles.

### Strict Portfolio Governance:
> [!IMPORTANT]
> **Zero Credit-Burn Terminology:** Never mention temporary promotional credits, credit deadlines, or credit burning in any documentation file (`docs/`), code comment, commit message, or portfolio artifact.
>
> All cost discussions must be framed in standard enterprise engineering terms:
> - **Cost Optimization:** "Serverless architecture engineered to operate at \$0.00 idle cost."
> - **Resource Efficiency:** "Batched asynchronous Document AI pipelines to minimize API invocation overhead."
> - **Free Tier Resilience:** "Architected to survive within Google Cloud permanent Free Tier quotas post-deployment."

---

## 2. Phase Documentation Structure

Every phase of the project must be documented in a dedicated markdown file under `docs/phases/` according to the following standard template:

### Standard Phase Document Sections:
1. **Executive Overview & Objective:**
   - What capability is being built.
   - Dual-track alignment (Data Engineering vs. Autonomous GenAI).
2. **Architecture Blueprint & Data Flow:**
   - Mermaid diagram depicting data inputs, processing stages, storage engines, and outputs.
3. **Engineering Trade-offs & Alternatives Considered:**
   - Comparison matrix (e.g., *Document AI Layout Parser vs. RecursiveCharacterTextSplitter*, *BigQuery Vector Search vs. Dedicated Pinecone/Vertex Endpoints*).
   - Justification for the selected design.
4. **Step-by-Step Implementation Guide:**
   - Complete, reproducible CLI commands (`gcloud`, `bq`).
   - Idiomatic Python code with type annotations, docstrings, and robust error handling.
5. **Verification & Testing Protocol:**
   - Exact queries, test scripts, and validation criteria.
   - Log excerpts proving operational success.
6. **CV Metric Bullets & Interview Talking Points:**
   - Bullet points ready for technical resumes (`bullet_bank.md`).
   - Deep-dive technical interview questions and high-impact answers.

---

## 3. Directory Layout for Documentation

```text
docs/
├── ARCHITECTURE.md                  # Master end-to-end architecture & design
├── phases/
│   ├── 00_agentic_scaffold_and_workflow.md    # Multi-agent scaffold & QA protocol
│   ├── 01_gcp_foundation_and_storage.md       # GCS Lakehouse, IAM & BigQuery
│   ├── 02_sec_ingestion_and_docai.md          # Layout Parser batch ETL
│   ├── 03_bigquery_vector_search_and_embeddings.md # 768-dim embeddings & SQL vector search
│   ├── 04_agentic_supervisor_and_tools.md     # Gemini 2.0 supervisor & tool calling
│   ├── 05_genai_evaluation_suite.md           # Vertex AI GenAI Eval metrics
│   ├── 06_streamlit_serving_and_cloud_run.md  # Containerized UI & Cloud Run
│   └── 07_cv_and_interview_talking_points.md  # Resume bank & interview mastery
└── benchmarks/
    ├── eval_results_v1.csv          # Per-question groundedness & faithfulness scores
    └── summary_metrics_v1.json      # Aggregate benchmark results
```
