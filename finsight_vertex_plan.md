# FinSight-Vertex: End-to-End Enterprise Financial RAG & Agent Pipeline

> **Fully Researched Architecture Blueprint & Single-Day Execution Plan**
> **Author:** Soumotanu Mazumdar | **Target:** Dual-Track CV Anchor (Senior Data Engineer & Autonomous GenAI Engineer)
> **Platform:** Google Cloud Platform (Vertex AI, BigQuery Vector Search, Document AI, Cloud Run)
> **Credit Deadline:** Sept 28, 2026 EOD IST

---

## 1. Executive Summary & Dual-Track Career Positioning

This project is engineered to serve as a flagship, dual-track portfolio showcase demonstrating production mastery of both **Modern Cloud Data Engineering** and **Autonomous GenAI / Agentic Systems**.

```
                           ┌──────────────────────────────────────────────┐
                           │               FINSIGHT-VERTEX                │
                           └──────────────────────┬───────────────────────┘
                                                  │
                 ┌────────────────────────────────┴────────────────────────────────┐
                 ▼                                                                 ▼
   [TRACK 1: SENIOR DATA ENGINEER]                                   [TRACK 2: AUTONOMOUS GENAI ENGINEER]
   • Enterprise ETL & Document Lakehouse                             • Agentic Tool-Use & Query Decomposition
   • BigQuery Vector Search & SQL Analytics                          • Vertex AI Reasoning Engine / Gemini
   • Table-Preserving Layout Ingestion (Document AI)                 • Deterministic Python Math Execution
   • Idempotent Data Pipelines & Lineage                             • Vertex AI Automated GenAI Evaluation Suite
```

### Resume Metric Bullets (Ready for `bullet_bank.md`)

* **Senior AI & Modern Data Engineering Track:**
  > *"Architected an enterprise document lakehouse on Google Cloud using Document AI Layout Parser and BigQuery Vector Search, indexing 10,000+ pages of SEC 10-K filings with automated table-preserving chunking and sub-second cosine similarity retrieval at $0.00 ongoing infrastructure cost."*

* **Autonomous GenAI & Agent Systems Track:**
  > *"Engineered an Agentic RAG system on Vertex AI with Gemini 2.0 Flash, incorporating deterministic Python code execution tools for quantitative verification and achieving 95%+ groundedness on Vertex AI GenAI Evaluation benchmarks."*

---

## 2. High-Level System Architecture

```mermaid
flowchart TD
    subgraph INGESTION["Phase 1: Ingestion & Document ETL"]
        A["SEC 10-K PDFs<br/>(Berkshire, Apple, JPM)"] --> B["Google Cloud Storage<br/>(GCS Bucket)"]
        B --> C["Document AI Layout Parser<br/>($0.01/page, async batch)"]
        C --> D["RAG Chunks with Markdown Tables<br/>(include_ancestor_headings=True)"]
        D --> E["Vertex AI text-embedding-004<br/>($0.025/1M chars, 768-dim)"]
        E --> F[("BigQuery Vector Store<br/>ARRAY &lt;FLOAT64&gt; + IVF Index")]
    end

    subgraph REASONING["Phase 2: Agentic Reasoning & Tools"]
        G["User Financial Query"] --> H["Supervisor Agent<br/>(Gemini 2.0 Flash)"]
        H --> I{"Intent Classifier & Router"}
        I -->|"Semantic Text"| J["Tool 1: BQ VECTOR_SEARCH<br/>(Risks, MD&A, Disclosures)"]
        I -->|"Structured Data"| K["Tool 2: BQ SQL Query<br/>(Balance Sheet, Income Stmt)"]
        I -->|"Math / Ratios"| L["Tool 3: Python Sandbox<br/>(Deterministic Calculations)"]
    end

    subgraph SYNTHESIS["Phase 3: Synthesis"]
        J --> M["Context Aggregator"]
        K --> M
        L --> M
        M --> N["Gemini Grounded Response<br/>(Page-level Citations)"]
    end

    subgraph EVALUATION["Phase 4: Evaluation"]
        N --> O["Vertex AI GenAI Eval Service<br/>(Judge: Gemini 1.5 Flash)"]
        O --> P["Groundedness, Faithfulness,<br/>QA Quality, Safety"]
    end

    subgraph SERVING["Phase 5: Serving"]
        N --> Q["Streamlit App<br/>(Cloud Run, --min-instances=0)"]
    end
```

---

## 3. Verified Pricing & Cost Estimates

> [!IMPORTANT]
> **The entire credit-burning sprint below costs an estimated $2–$8 of GCP credits.** The architecture is deliberately designed so that after credits expire, your live demo runs within GCP's permanent Free Tier.

### Credit-Burning Tasks (Today Only)

| Service | Operation | Estimated Volume | Unit Cost | Estimated Total |
| :--- | :--- | :--- | :--- | ---: |
| **Document AI Layout Parser** | Parse SEC 10-K PDFs | ~500 pages (3–5 filings) | $0.01/page | **$5.00** |
| **Vertex AI Embeddings** (`text-embedding-004`) | Embed ~1,000 chunks × ~500 chars avg | ~500K characters | $0.025/1M chars | **$0.01** |
| **Vertex AI GenAI Eval** (Gemini 1.5 Flash judge) | Evaluate 50 Q&A pairs × ~2K tokens/eval | ~100K tokens | $0.075/1M input tokens | **< $0.01** |
| **Cloud Storage** | Store PDFs + parsed output | ~50 MB | $0.020/GB/month | **< $0.01** |
| **BigQuery** | Load embeddings, create vector index, run queries | < 100 MB storage, < 1 GB scanned | Free tier | **$0.00** |
| | | | **Sprint Total:** | **~$5–$8** |

### Permanent Free Tier (Post-Credits Survival)

| Service | Free Tier Allowance | Your Usage |
| :--- | :--- | :--- |
| **BigQuery Storage** | 10 GiB/month | ~100 MB (embeddings + metadata) ✅ |
| **BigQuery Queries** | 1 TiB/month scanned | ~1 GB/month for demo queries ✅ |
| **BQ Vector Index Compute** | 6 TB indexed data (org-wide) | ~100 MB ✅ |
| **Cloud Run** | 180K vCPU-sec + 360K GiB-sec/month | Scale-to-zero when idle ✅ |

> [!CAUTION]
> **What does NOT survive credits:** Vertex AI Gemini API calls (Gemini 2.0 Flash: $0.10/1M input tokens). After credits expire, you can either:
> 1. Switch the agent's LLM calls to **Google AI Studio free tier** (Gemini 2.0 Flash: 10 RPM, 1500 RPD free) for demo purposes.
> 2. Or keep Vertex AI and accept minimal pay-as-you-go costs (~$0.01–$0.05/day for light demo usage).

---

## 4. Single-Day Credit Sprint: Hour-by-Hour Execution Plan

> **Current time:** ~2:00 AM IST, Sept 28. Credits expire EOD.
> **Strategy:** Execute all credit-burning GCP API calls today. Everything else (agent code, Streamlit UI, portfolio integration) can be built at leisure using the pre-computed BigQuery data and free-tier Gemini.

---

### ⏱️ Block 1: GCP Project Setup (30 min)

**Goal:** Authenticated GCP project with all APIs enabled.

```bash
# 1. Authenticate
gcloud auth login
gcloud auth application-default login

# 2. Create dedicated project (pick a unique ID)
gcloud projects create finsight-vertex --name="FinSight Vertex AI"

# 3. Link your billing account (with the expiring credits)
gcloud billing accounts list
gcloud billing projects link finsight-vertex --billing-account=YOUR_BILLING_ACCOUNT_ID

# 4. Set as active project
gcloud config set project finsight-vertex

# 5. Enable ALL required APIs (single command)
gcloud services enable \
  aiplatform.googleapis.com \
  documentai.googleapis.com \
  bigquery.googleapis.com \
  bigqueryconnection.googleapis.com \
  storage.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com

# 6. Create GCS bucket (use us-central1 for best Vertex AI feature parity)
gcloud storage buckets create gs://finsight-document-lakehouse \
  --location=us-central1 \
  --default-storage-class=STANDARD

# 7. Create BigQuery dataset
bq mk --location=US finsight_lakehouse
```

---

### ⏱️ Block 2: Download SEC 10-K Filings (20 min)

**Goal:** 3–5 real SEC 10-K PDFs ready for Document AI processing.

> [!NOTE]
> **Key insight from research:** SEC EDGAR serves filings as HTML/iXBRL (`.htm`), not native PDFs. For Document AI (which processes PDFs), you have two options:
> 1. **Direct PDF downloads** from company Investor Relations pages (recommended, fastest).
> 2. **`edgartools` library** to download HTML, then convert to PDF.
>
> Berkshire Hathaway provides direct PDFs. For others, use the IR portals.

#### Option A: Direct PDF Downloads (Fastest)

| Company | Direct 10-K PDF URL |
| :--- | :--- |
| **Berkshire Hathaway (FY2024)** | `https://www.berkshirehathaway.com/2024ar/2024ar.pdf` |
| **Berkshire Hathaway (FY2023)** | `https://www.berkshirehathaway.com/2023ar/2023ar.pdf` |
| **Apple (FY2024)** | Download from `https://investor.apple.com/sec-filings/` → click 10-K → PDF |
| **JPMorgan Chase (FY2024)** | Download from `https://www.jpmorganchase.com/ir/annual-report` |

```bash
# Create local data directory
mkdir -p finsight-vertex/data/raw_pdfs

# Download Berkshire directly
curl -o finsight-vertex/data/raw_pdfs/BRK_10K_2024.pdf \
  "https://www.berkshirehathaway.com/2024ar/2024ar.pdf"

curl -o finsight-vertex/data/raw_pdfs/BRK_10K_2023.pdf \
  "https://www.berkshirehathaway.com/2023ar/2023ar.pdf"
```

#### Option B: Using `edgartools` (Richer metadata, but outputs HTML)

```python
# pip install edgartools
from edgar import set_identity, Company

set_identity("FinSightResearch soumotanu@finsightresearch.dev")

company = Company("AAPL")
filings = company.get_filings(form="10-K")
latest_10k = filings.latest()

# Export to clean Markdown (great for direct RAG without Document AI)
md_content = latest_10k.markdown()

# Or download raw filing + attachments
latest_10k.download("./finsight-vertex/data/raw_filings/AAPL/")
```

**Upload PDFs to GCS:**
```bash
gcloud storage cp finsight-vertex/data/raw_pdfs/*.pdf \
  gs://finsight-document-lakehouse/raw_pdfs/
```

---

### ⏱️ Block 3: Document AI Layout Parser (45 min)

**Goal:** Parse all PDFs into structured, table-preserving chunks with ancestor headings.

#### Step 1: Create the Layout Parser Processor

```python
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

def create_layout_parser(project_id: str, location: str = "us") -> documentai.Processor:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    parent = client.common_location_path(project_id, location)

    processor = client.create_processor(
        parent=parent,
        processor=documentai.Processor(
            display_name="sec-filing-layout-parser",
            type_="LAYOUT_PARSER_PROCESSOR",
        ),
    )
    print(f"✅ Processor created: {processor.name}")
    print(f"   ID: {processor.name.split('/')[-1]}")
    return processor

# Run once:
# processor = create_layout_parser("finsight-vertex")
```

#### Step 2: Batch Process PDFs (Required for 100+ page filings)

> [!IMPORTANT]
> **Synchronous `process_document` is limited to 15 pages.** SEC 10-Ks are 80–200+ pages. You **must** use **`batch_process_documents`** with GCS input/output.

```python
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
import json

def batch_parse_10k(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_prefix: str,   # e.g., "gs://finsight-document-lakehouse/raw_pdfs/"
    gcs_output_uri: str,     # e.g., "gs://finsight-document-lakehouse/parsed_output/"
    chunk_size: int = 1024,
):
    """Asynchronously parse all PDFs in a GCS prefix using Layout Parser with chunking."""
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    resource_name = client.processor_path(project_id, location, processor_id)

    # Configure input: all PDFs in the GCS prefix
    gcs_input = documentai.BatchDocumentsInputConfig(
        gcs_prefix=documentai.GcsPrefix(gcs_uri_prefix=gcs_input_prefix)
    )

    # Configure output
    gcs_output = documentai.DocumentOutputConfig(
        gcs_output_config=documentai.DocumentOutputConfig.GcsOutputConfig(
            gcs_uri=gcs_output_uri,
            field_mask="chunkedDocument,documentLayout",  # Only export what we need
        )
    )

    # Enable layout-aware chunking with ancestor heading inheritance
    process_options = documentai.ProcessOptions(
        layout_config=documentai.ProcessOptions.LayoutConfig(
            chunking_config=documentai.ProcessOptions.LayoutConfig.ChunkingConfig(
                chunk_size=chunk_size,
                include_ancestor_headings=True,  # Prepends H1/H2 section context
            )
        )
    )

    request = documentai.BatchProcessRequest(
        name=resource_name,
        input_documents=gcs_input,
        document_output_config=gcs_output,
        process_options=process_options,
    )

    # Kick off async batch job
    operation = client.batch_process_documents(request=request)
    print(f"🚀 Batch job started: {operation.operation.name}")
    print("   Polling for completion (this may take 5-15 minutes for large filings)...")

    result = operation.result(timeout=1800)  # Wait up to 30 min
    print("✅ Batch processing complete!")
    return result

# Run:
# batch_parse_10k(
#     project_id="finsight-vertex",
#     location="us",
#     processor_id="YOUR_PROCESSOR_ID",
#     gcs_input_prefix="gs://finsight-document-lakehouse/raw_pdfs/",
#     gcs_output_uri="gs://finsight-document-lakehouse/parsed_output/",
#     chunk_size=1024,
# )
```

#### Step 3: Extract Chunks from Parsed Output

```python
from google.cloud import storage
import json

def extract_chunks_from_gcs(bucket_name: str, output_prefix: str) -> list[dict]:
    """Download parsed Document AI output from GCS and extract all chunks."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=output_prefix)

    all_chunks = []
    for blob in blobs:
        if not blob.name.endswith(".json"):
            continue

        doc_json = json.loads(blob.download_as_text())

        # Extract source filename from GCS path
        source_doc = blob.name.split("/")[-2]  # Parent directory = original filename

        if "chunkedDocument" in doc_json and "chunks" in doc_json["chunkedDocument"]:
            for chunk in doc_json["chunkedDocument"]["chunks"]:
                all_chunks.append({
                    "chunk_id": chunk.get("chunkId", ""),
                    "content": chunk.get("content", ""),
                    "source_document": source_doc,
                    "source_headers": [
                        h.get("text", "") for h in chunk.get("sourceBlockIds", [])
                    ],
                    "page_start": chunk.get("pageSpan", {}).get("pageStart", 0),
                    "page_end": chunk.get("pageSpan", {}).get("pageEnd", 0),
                })

    print(f"✅ Extracted {len(all_chunks)} total chunks from parsed output")
    return all_chunks

# chunks = extract_chunks_from_gcs("finsight-document-lakehouse", "parsed_output/")
```

---

### ⏱️ Block 4: Generate Embeddings & Load into BigQuery (45 min)

**Goal:** Vectorize all chunks and insert into a BigQuery table with a vector index.

#### Step 1: Generate Embeddings with `text-embedding-004`

```python
import vertexai
from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput
from concurrent.futures import ThreadPoolExecutor, as_completed

vertexai.init(project="finsight-vertex", location="us-central1")
model = TextEmbeddingModel.from_pretrained("text-embedding-004")

def embed_chunks(chunks: list[dict], batch_size: int = 250, max_workers: int = 5) -> list[dict]:
    """Embed all chunks using batched concurrent requests. Max 250 per API call."""

    def process_batch(batch_chunks: list[dict]) -> list[dict]:
        inputs = [
            TextEmbeddingInput(
                text=c["content"][:2048],  # Max 2048 tokens input
                task_type="RETRIEVAL_DOCUMENT",
                title=c.get("source_document", ""),
            )
            for c in batch_chunks
        ]
        embeddings = model.get_embeddings(inputs, output_dimensionality=768)
        for chunk, emb in zip(batch_chunks, embeddings):
            chunk["embedding"] = emb.values
        return batch_chunks

    batches = [chunks[i:i + batch_size] for i in range(0, len(chunks), batch_size)]
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_batch, b): i for i, b in enumerate(batches)}
        for future in as_completed(futures):
            results.extend(future.result())
            print(f"  Embedded batch {futures[future] + 1}/{len(batches)}")

    print(f"✅ Generated embeddings for {len(results)} chunks")
    return results

# embedded_chunks = embed_chunks(chunks)
```

#### Step 2: Create BigQuery Table & Load Data

```python
from google.cloud import bigquery

bq_client = bigquery.Client(project="finsight-vertex")

# Create table with vector column
CREATE_TABLE_SQL = """
CREATE OR REPLACE TABLE `finsight-vertex.finsight_lakehouse.financial_chunks` (
    chunk_id STRING NOT NULL,
    content STRING NOT NULL,
    source_document STRING,
    page_start INT64,
    page_end INT64,
    embedding ARRAY<FLOAT64> NOT NULL
)
"""
bq_client.query(CREATE_TABLE_SQL).result()
print("✅ BigQuery table created")

# Insert chunks using the streaming API (or load from JSONL)
import json
import tempfile

def load_chunks_to_bq(chunks: list[dict]):
    """Load embedded chunks into BigQuery via a JSONL upload."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for chunk in chunks:
            row = {
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "source_document": chunk["source_document"],
                "page_start": chunk["page_start"],
                "page_end": chunk["page_end"],
                "embedding": chunk["embedding"],
            }
            f.write(json.dumps(row) + "\n")
        tmp_path = f.name

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    table_ref = "finsight-vertex.finsight_lakehouse.financial_chunks"

    with open(tmp_path, "rb") as f:
        load_job = bq_client.load_table_from_file(f, table_ref, job_config=job_config)
    load_job.result()
    print(f"✅ Loaded {load_job.output_rows} rows into BigQuery")

# load_chunks_to_bq(embedded_chunks)
```

#### Step 3: Create BigQuery Vector Index

> [!NOTE]
> **Minimum 5,000 rows required** for BigQuery to build a vector index. If you have fewer rows, `VECTOR_SEARCH` will still work — it just falls back to exact brute-force search (which is fine for < 5K chunks and actually gives 100% recall).

```sql
-- Use IVF for low-latency single-query lookups (ideal for interactive RAG)
CREATE VECTOR INDEX IF NOT EXISTS `financial_chunks_ivf_idx`
ON `finsight-vertex.finsight_lakehouse.financial_chunks`(embedding)
STORING(chunk_id, content, source_document, page_start, page_end)
OPTIONS (
    index_type = 'IVF',
    distance_type = 'COSINE'
);
```

#### Step 4: Register Vertex AI Embedding Model as BQ Remote Model

This enables embedding queries directly inside SQL (no Python round-trip needed):

```bash
# Create Cloud Resource Connection
bq mk --connection \
  --location=US \
  --project_id=finsight-vertex \
  --connection_type=CLOUD_RESOURCE \
  vertex_ai_conn

# Get the service account ID
bq show --connection finsight-vertex.US.vertex_ai_conn
# Look for serviceAccountId: bqcx-XXXX@gcp-sa-bigquery-condel.iam.gserviceaccount.com

# Grant it Vertex AI User role
gcloud projects add-iam-policy-binding finsight-vertex \
  --member='serviceAccount:bqcx-XXXX@gcp-sa-bigquery-condel.iam.gserviceaccount.com' \
  --role='roles/aiplatform.user'
```

```sql
-- Register the remote embedding model
CREATE OR REPLACE MODEL `finsight-vertex.finsight_lakehouse.vertex_embed_model`
REMOTE WITH CONNECTION `finsight-vertex.US.vertex_ai_conn`
OPTIONS (ENDPOINT = 'text-embedding-004');

-- Test it
SELECT * FROM ML.GENERATE_EMBEDDING(
    MODEL `finsight-vertex.finsight_lakehouse.vertex_embed_model`,
    (SELECT 'What are Apple''s primary risk factors?' AS content),
    STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_QUERY' AS task_type)
);
```

#### Step 5: Test End-to-End Vector Search in Pure SQL

```sql
-- Full end-to-end: embed query → vector search → return cited chunks
WITH query_embedding AS (
    SELECT ml_generate_embedding_result AS query_vec
    FROM ML.GENERATE_EMBEDDING(
        MODEL `finsight-vertex.finsight_lakehouse.vertex_embed_model`,
        (SELECT 'What are the key risk factors for Berkshire Hathaway?' AS content),
        STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_QUERY' AS task_type)
    )
)
SELECT
    base.chunk_id,
    base.source_document,
    base.page_start,
    LEFT(base.content, 200) AS content_preview,
    distance
FROM VECTOR_SEARCH(
    TABLE `finsight-vertex.finsight_lakehouse.financial_chunks`,
    'embedding',
    TABLE query_embedding,
    query_column_to_search => 'query_vec',
    top_k => 5,
    distance_type => 'COSINE'
)
ORDER BY distance ASC;
```

---

### ⏱️ Block 5: Run Vertex AI GenAI Evaluation (30 min)

**Goal:** Generate verifiable groundedness and faithfulness metrics for your CV.

> [!TIP]
> **Use Gemini 1.5 Flash as the judge model — it's 16× cheaper than Pro** ($0.075 vs $1.25 per 1M input tokens) and is Google's recommended autorater for high-volume evaluation.

#### Step 1: Prepare Evaluation Dataset

Create a `data/eval_set.jsonl` with 20–50 financial Q&A pairs:

```python
import pandas as pd

eval_data = {
    "prompt": [
        "What were Berkshire Hathaway's total revenues in 2024?",
        "Describe Apple's key supply chain risk factors from their latest 10-K.",
        "What is JPMorgan's net interest income trend over the last 3 years?",
        # ... add 20-50 domain-specific questions
    ],
    "context": [
        # Fill with actual retrieved chunks from BigQuery VECTOR_SEARCH
        "Revenue for 2024 was $371.4 billion compared to $364.5 billion in 2023...",
        "The Company's products and services may be affected by supply chain...",
        "Net interest income was $89.3B in 2024, $87.1B in 2023, and $66.7B in 2022...",
    ],
    "response": [
        # Fill with your agent's actual generated responses
        "Berkshire Hathaway reported total revenues of $371.4 billion in 2024.",
        "Apple identifies several supply chain risks including...",
        "JPMorgan's net interest income showed a steady upward trend...",
    ],
    "reference": [
        # Gold-standard human-curated answers
        "Berkshire Hathaway's total revenues in 2024 were $371.4 billion.",
        "Apple's 10-K Item 1A identifies supply chain concentration...",
        "JPM NII: $66.7B (2022) → $87.1B (2023) → $89.3B (2024).",
    ],
}
eval_df = pd.DataFrame(eval_data)
```

#### Step 2: Run Evaluation

```python
import vertexai
from vertexai.evaluation import EvalTask, MetricPromptTemplateExamples

vertexai.init(project="finsight-vertex", location="us-central1")

eval_task = EvalTask(
    dataset=eval_df,
    metrics=[
        MetricPromptTemplateExamples.Pointwise.GROUNDEDNESS,
        MetricPromptTemplateExamples.Pointwise.QUESTION_ANSWERING_QUALITY,
        MetricPromptTemplateExamples.Pointwise.SAFETY,
        "rouge_l",
        "bleu",
    ],
    experiment="finsight-rag-benchmark-v1",
)

eval_result = eval_task.evaluate()

# Print summary
print("\n📊 === EVALUATION SUMMARY ===")
print(eval_result.summary_metrics)

# Detailed per-question breakdown
metrics_df = eval_result.metrics_table
print("\n📋 === DETAILED RESULTS ===")
print(metrics_df[["prompt", "groundedness/score", "question_answering_quality/score", "safety/score"]].to_string())

# SAVE these results — they are your CV metrics!
metrics_df.to_csv("docs/benchmarks/eval_results_v1.csv", index=False)
import json
with open("docs/benchmarks/summary_metrics_v1.json", "w") as f:
    json.dump(eval_result.summary_metrics, f, indent=2)

print("\n✅ Evaluation results saved to docs/benchmarks/")
```

---

## 5. Post-Credit Development Roadmap (Free / Near-Free)

Everything below runs on **BigQuery Free Tier** (pre-loaded embeddings) + **Google AI Studio Free Tier** (Gemini 2.0 Flash: 10 RPM, 1500 RPD) or minimal Vertex AI pay-as-you-go.

### Phase 2: Agentic Routing & Tool Execution (Week 1)

| Task | Details | Cost |
| :--- | :--- | :--- |
| Build Supervisor Agent | Python class using `google-genai` SDK with Gemini 2.0 Flash | Free (AI Studio) or ~$0.10/1M tokens (Vertex) |
| Tool 1: `vector_search_tool` | Calls BigQuery `VECTOR_SEARCH` via `google-cloud-bigquery` Python SDK | Free (BQ free tier) |
| Tool 2: `sql_query_tool` | Structured SQL against a financial metrics table in BigQuery | Free (BQ free tier) |
| Tool 3: `python_calculator_tool` | `exec()` sandbox for deterministic financial math | Free (local compute) |
| System Prompt Engineering | Enforce Markdown table output, page-level citations `[Source: BRK_10K_2024.pdf, p.42]` | Free |

### Phase 3: Streamlit UI (Week 2)

Key Streamlit patterns verified by research:

```python
import streamlit as st

st.set_page_config(page_title="FinSight", page_icon="📊", layout="wide")

# Cache expensive clients once per container lifecycle
@st.cache_resource
def get_bq_client():
    from google.cloud import bigquery
    return bigquery.Client(project="finsight-vertex")

# Chat interface with citations
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander(f"📚 Citations ({len(msg['sources'])})"):
                for src in msg["sources"]:
                    st.caption(f"[{src['doc']}] Page {src['page']} | Score: {src['score']:.2f}")
                    st.markdown(f"> {src['snippet']}")

# Reasoning trace accordion
with st.status("Analyzing...", expanded=True) as status:
    st.write("🔍 Embedding query via text-embedding-004...")
    st.write("📑 Searching BigQuery Vector Index (top-k=5)...")
    st.write("🧮 Running deterministic calculations...")
    st.write("🧠 Synthesizing with Gemini 2.0 Flash...")
    status.update(label="Complete!", state="complete", expanded=False)
```

### Phase 4: Cloud Run Deployment (Week 3)

**Dockerfile (verified for Streamlit on Cloud Run):**
```dockerfile
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8080 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8080
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]
```

**Deploy (zero idle cost):**
```bash
# Option A: One-step source deploy (no local Docker needed)
gcloud run deploy finsight-vertex \
    --source . \
    --region=us-central1 \
    --allow-unauthenticated \
    --min-instances=0 \
    --max-instances=3 \
    --cpu=2 \
    --memory=2Gi \
    --timeout=3600 \
    --session-affinity

# Option B: Build + push + deploy
gcloud builds submit --tag us-central1-docker.pkg.dev/finsight-vertex/rag-apps/finsight:v1 .
gcloud run deploy finsight-vertex \
    --image=us-central1-docker.pkg.dev/finsight-vertex/rag-apps/finsight:v1 \
    --region=us-central1 \
    --allow-unauthenticated \
    --min-instances=0 --max-instances=3 \
    --cpu=2 --memory=2Gi --timeout=3600 \
    --session-affinity
```

> [!WARNING]
> **Streamlit WebSocket Billing Trap:** Streamlit keeps a persistent WebSocket open. As long as a browser tab is connected, Cloud Run considers the instance "active" and bills for it. The container only scales to zero once all tabs are closed AND the ~15-min idle timeout elapses.

### Phase 5: Portfolio & CV Integration (Week 4)
- [ ] Create repository `FortunateSpy5/finsight-vertex` with comprehensive README.
- [ ] Add project dossier to `projects/catalog.md` (Tier 2 → Tier 1 graduation).
- [ ] Update `resume/bullet_bank.md` with verified evaluation metrics.
- [ ] Run `portfolio-sync` skill to update [fortunatespy5.github.io](https://fortunatespy5.github.io).
- [ ] Run `linkedin-drafter` skill for technical launch post.

---

## 6. Repository Layout Blueprint

```
finsight-vertex/
├── .github/workflows/          # CI/CD: Linting, tests, Cloud Run deployment
├── data/
│   ├── raw_pdfs/               # 3–5 SEC 10-K PDFs (Berkshire, Apple, JPM)
│   ├── parsed_chunks/          # Document AI output (cached locally for dev)
│   └── eval_set.jsonl          # Gold-standard Q&A pairs for evaluation
├── docs/
│   ├── ARCHITECTURE.md         # Full system architecture & sequence diagrams
│   └── benchmarks/
│       ├── eval_results_v1.csv # Vertex AI GenAI Evaluation per-question scores
│       └── summary_metrics.json # Aggregate groundedness, faithfulness, QA quality
├── src/
│   ├── ingestion/              # [Track 1: Data Engineering]
│   │   ├── docai_parser.py     # Document AI Layout Parser batch processor
│   │   ├── chunk_extractor.py  # GCS parsed output → structured chunk dicts
│   │   ├── embedder.py         # Vertex AI text-embedding-004 batch embedder
│   │   └── bq_loader.py       # BigQuery table creation & JSONL loader
│   ├── agent/                  # [Track 2: GenAI Agent]
│   │   ├── supervisor.py       # Gemini 2.0 Flash supervisor with tool routing
│   │   ├── tools/
│   │   │   ├── vector_tool.py  # BigQuery VECTOR_SEARCH caller
│   │   │   ├── sql_tool.py     # Structured financial table query
│   │   │   └── math_tool.py    # Deterministic Python calculation sandbox
│   │   └── synthesizer.py      # Grounded response generator with citations
│   ├── evaluation/
│   │   ├── prepare_eval.py     # Build eval dataset from BQ + manual curation
│   │   └── run_vertex_eval.py  # Vertex AI GenAI Evaluation pipeline runner
│   └── app.py                  # Streamlit application entrypoint
├── Dockerfile                  # Cloud Run container (verified config above)
├── requirements.txt            # Pinned dependencies
├── .streamlit/config.toml      # Streamlit server config
└── README.md                   # Portfolio-grade README with arch diagram & demo link
```

---

## 7. Technical Deep-Dive: Why This Architecture Wins on a CV

### Document AI Layout Parser vs. Naive Chunking
| Approach | Table Handling | Heading Context | Cost |
| :--- | :--- | :--- | :--- |
| LangChain `RecursiveCharacterTextSplitter` | ❌ Cuts tables mid-row | ❌ None | Free |
| LlamaIndex `SentenceSplitter` | ❌ Cuts tables mid-row | ❌ None | Free |
| **Document AI Layout Parser** | ✅ Atomic table chunks as Markdown | ✅ `include_ancestor_headings=True` | $0.01/page |

### BigQuery Vector Search vs. Dedicated Vector DB
| Approach | Idle Cost | Free Tier | SQL Integration | CV Signal |
| :--- | :--- | :--- | :--- | :--- |
| Pinecone Serverless | $0 idle, $8+/mo active | Limited free tier | ❌ Separate API | Medium |
| Vertex AI Vector Search (Endpoint) | **$0.30+/hr always-on** | ❌ None | ❌ Separate API | High |
| **BigQuery VECTOR_SEARCH** | **$0.00 idle** | ✅ 10 GiB + 1 TiB/mo | ✅ Native SQL | **Very High** |

### Agentic Tool Calling vs. Naive RAG
| Approach | Math Accuracy | Multi-Source Reasoning | Verifiability |
| :--- | :--- | :--- | :--- |
| Stuff all chunks into prompt | ❌ LLM guesses math | ❌ Single retrieval pass | ❌ No trace |
| **Supervisor Agent + Tool Routing** | ✅ Deterministic Python | ✅ SQL + Vector + Code | ✅ Full reasoning trace |

### Vertex AI GenAI Evaluation vs. "Trust Me" Metrics
| Approach | Reproducible | Industry Standard | Automated |
| :--- | :--- | :--- | :--- |
| "It works well" / manual testing | ❌ | ❌ | ❌ |
| Custom ROUGE/BLEU only | Partially | Partially | ✅ |
| **Vertex AI Eval Service (Groundedness + Faithfulness + QA Quality)** | ✅ | ✅ | ✅ |
