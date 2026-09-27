# Rule: Google Cloud Data Engineering Standards

This rule establishes strict enterprise data engineering standards across Google Cloud Storage, Document AI, BigQuery, and Vertex AI.

---

## 1. Document Lakehouse & GCS Architecture

- **Bucket Hierarchy:** Maintain clean prefix separation:
  - `gs://finsight-document-lakehouse/raw_pdfs/`: Original immutable SEC 10-K filings.
  - `gs://finsight-document-lakehouse/parsed_output/`: Asynchronous Document AI JSON outputs.
  - `gs://finsight-document-lakehouse/staging/`: Intermediate transformed JSONL datasets.
- **Storage Class:** Use `STANDARD` storage class located in `us-central1` for maximum Vertex AI and Document AI feature parity.
- **Idempotency:** All ingestion jobs must support re-runs without duplicate record creation in downstream BigQuery tables.

---

## 2. Document AI Layout Parser Governance

- **Async Batching Mandatory:** Because SEC 10-K filings contain 80–200+ pages, synchronous calls (`process_document`, capped at 15 pages) will fail. Always use `batch_process_documents` with GCS prefixes.
- **Layout & Table Preservation:**
  - `chunking_config` must enable `include_ancestor_headings = True` to inherit H1/H2 section contexts into each chunk.
  - Tables must be preserved as structured Markdown text rather than flattened or split arbitrarily mid-row.
- **Field Masks:** Use field masks (e.g., `chunkedDocument,documentLayout`) on Document AI export requests to minimize serialization overhead and avoid storing redundant raw OCR layout data.

---

## 3. BigQuery Vector Search & Analytics

- **Schema Design:**
  - Table: `finsight-vertex.finsight_lakehouse.financial_chunks`
  - Columns:
    - `chunk_id` (`STRING`, Primary key)
    - `content` (`STRING`, Textual chunk content with Markdown tables)
    - `source_document` (`STRING`, E.g., `BRK_10K_2024.pdf`)
    - `page_start` (`INT64`, Document start page)
    - `page_end` (`INT64`, Document end page)
    - `embedding` (`ARRAY<FLOAT64>`, 768 dimensions for `text-embedding-004`)
- **Vector Indexing:**
  - Index Type: `IVF` (Inverted File Flat) with `COSINE` distance.
  - Note: BigQuery requires 5,000+ rows to build index partitions. For smaller corpora (<5,000 chunks), BigQuery `VECTOR_SEARCH` automatically uses exact brute-force search with 100% recall.
- **Remote Model Integration:**
  - Register `text-embedding-004` as a BigQuery Remote Model connected via a Cloud Resource Connection (`vertex_ai_conn`).
  - Enables single-query embedding and vector retrieval inside BigQuery SQL via `ML.GENERATE_EMBEDDING` and `VECTOR_SEARCH`.
