"""BigQuery vector lakehouse loader and IVF index creator."""

import functools
import json
import logging
import os
from pathlib import Path
import re
import tempfile
import uuid
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

from src.config import settings
from src.ingestion.chunk_extractor import EmbeddedChunkRecord

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Strict identifier validation pattern (alphanumeric and underscores only)
IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")


def validate_identifier(name: str, identifier_type: str = "identifier") -> str:
    """Ensure identifier matches BigQuery strict naming rules to prevent DDL injection."""
    if not name or not IDENTIFIER_PATTERN.match(name):
        raise ValueError(
            f"Invalid {identifier_type}: '{name}'. Must consist only of alphanumeric characters and underscores."
        )
    return name


@functools.lru_cache(maxsize=1)
def get_bq_client(project_id: str = settings.PROJECT_ID) -> bigquery.Client:
    """Return a cached BigQuery client instance."""
    return bigquery.Client(project=project_id)


def create_chunks_table(
    client: bigquery.Client,
    dataset_id: str = settings.BQ_DATASET,
    table_id: str = settings.BQ_CHUNKS_TABLE,
) -> bigquery.Table:
    """Create the financial_chunks BigQuery table supporting vector search."""
    validate_identifier(dataset_id, "dataset_id")
    validate_identifier(table_id, "table_id")

    full_table_id = f"{client.project}.{dataset_id}.{table_id}"
    schema = [
        bigquery.SchemaField("chunk_id", "STRING", mode="REQUIRED", description="Unique chunk identifier"),
        bigquery.SchemaField("content", "STRING", mode="REQUIRED", description="Preserved text and Markdown table"),
        bigquery.SchemaField("source_document", "STRING", mode="NULLABLE", description="Source filing PDF name"),
        bigquery.SchemaField("page_start", "INTEGER", mode="NULLABLE", description="Starting page in document"),
        bigquery.SchemaField("page_end", "INTEGER", mode="NULLABLE", description="Ending page in document"),
        bigquery.SchemaField(
            "embedding",
            "FLOAT64",
            mode="REPEATED",
            description="768-dimensional Vertex AI text-embedding-004 vector",
        ),
    ]

    table = bigquery.Table(full_table_id, schema=schema)
    try:
        existing_table = client.get_table(full_table_id)
        logger.info(f"Table {full_table_id} already exists.")
        return existing_table
    except NotFound:
        logger.info(f"Creating table {full_table_id}...")
        created_table = client.create_table(table)
        logger.info(f"Successfully created BigQuery table: {created_table.full_table_id}")
        return created_table


def load_chunks_to_bigquery(
    client: bigquery.Client,
    chunks: list[EmbeddedChunkRecord],
    dataset_id: str = settings.BQ_DATASET,
    table_id: str = settings.BQ_CHUNKS_TABLE,
    truncate: bool = False,
) -> int:
    """Load embedded chunks into BigQuery using NDJSON batch load.

    Safely removes temporary NDJSON staging files in a finally block.

    Args:
        client: BigQuery client.
        chunks: List of chunk dictionaries containing 'embedding'.
        dataset_id: Target BigQuery dataset.
        table_id: Target BigQuery table.
        truncate: Whether to truncate the table before loading.

    Returns:
        Number of rows loaded.
    """
    validate_identifier(dataset_id, "dataset_id")
    validate_identifier(table_id, "table_id")

    table_ref = f"{client.project}.{dataset_id}.{table_id}"
    logger.info(f"Staging {len(chunks)} chunks to temporary NDJSON file...")

    tmp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
        ) as tmp:
            for chunk in chunks:
                row = {
                    "chunk_id": chunk["chunk_id"],
                    "content": chunk["content"],
                    "source_document": chunk.get("source_document", ""),
                    "page_start": chunk.get("page_start", 1),
                    "page_end": chunk.get("page_end", 1),
                    "embedding": chunk["embedding"],
                }
                tmp.write(json.dumps(row, ensure_ascii=False) + "\n")
            tmp_path = tmp.name

        write_disp = (
            bigquery.WriteDisposition.WRITE_TRUNCATE
            if truncate
            else bigquery.WriteDisposition.WRITE_APPEND
        )

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=write_disp,
        )

        logger.info(f"Submitting BigQuery load job for {table_ref}...")
        with open(tmp_path, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

        job.result()
        logger.info(f"Load job completed. Inserted {job.output_rows} rows into {table_ref}.")
        return job.output_rows or 0
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError as err:
                logger.warning(f"Failed to remove temporary file {tmp_path}: {err}")


def upsert_chunks_to_bigquery(
    client: bigquery.Client,
    chunks: list[EmbeddedChunkRecord],
    dataset_id: str = settings.BQ_DATASET,
    table_id: str = settings.BQ_CHUNKS_TABLE,
) -> int:
    """Idempotently upsert embedded chunks into BigQuery using an atomic MERGE.

    Prevents duplicate chunks during retries or re-indexing runs.
    """
    validate_identifier(dataset_id, "dataset_id")
    validate_identifier(table_id, "table_id")

    # Ensure base target table exists
    create_chunks_table(client, dataset_id, table_id)

    # Create temporary staging table with random suffix
    staging_suffix = f"stage_{uuid.uuid4().hex[:8]}"
    stage_table_id = f"{table_id}_{staging_suffix}"
    create_chunks_table(client, dataset_id, stage_table_id)

    try:
        # Load batch into staging table
        load_chunks_to_bigquery(client, chunks, dataset_id, stage_table_id, truncate=True)

        target_ref = f"`{client.project}.{dataset_id}.{table_id}`"
        stage_ref = f"`{client.project}.{dataset_id}.{stage_table_id}`"

        merge_sql = f"""
        MERGE {target_ref} T
        USING {stage_ref} S
        ON T.chunk_id = S.chunk_id
        WHEN MATCHED THEN
            UPDATE SET
                content = S.content,
                source_document = S.source_document,
                page_start = S.page_start,
                page_end = S.page_end,
                embedding = S.embedding
        WHEN NOT MATCHED THEN
            INSERT (chunk_id, content, source_document, page_start, page_end, embedding)
            VALUES (S.chunk_id, S.content, S.source_document, S.page_start, S.page_end, S.embedding);
        """
        logger.info(f"Executing atomic MERGE from {stage_ref} into {target_ref}...")
        merge_job = client.query(merge_sql)
        merge_job.result()
        logger.info(f"Atomic MERGE completed successfully for {len(chunks)} chunks.")
        return len(chunks)
    finally:
        client.delete_table(f"{client.project}.{dataset_id}.{stage_table_id}", not_found_ok=True)


def create_vector_index(
    client: bigquery.Client,
    dataset_id: str = settings.BQ_DATASET,
    table_id: str = settings.BQ_CHUNKS_TABLE,
    index_name: str = "financial_chunks_ivf_idx",
) -> None:
    """Create an IVF Cosine Vector Index on the financial_chunks table.

    Validates all identifiers against DDL injection before execution.
    """
    validate_identifier(dataset_id, "dataset_id")
    validate_identifier(table_id, "table_id")
    validate_identifier(index_name, "index_name")

    full_table_id = f"`{client.project}.{dataset_id}.{table_id}`"
    sql = f"""
    CREATE VECTOR INDEX IF NOT EXISTS `{index_name}`
    ON {full_table_id}(embedding)
    STORING(chunk_id, content, source_document, page_start, page_end)
    OPTIONS (
        index_type = 'IVF',
        distance_type = 'COSINE'
    );
    """
    logger.info(f"Executing vector index creation on {full_table_id}...")
    try:
        query_job = client.query(sql)
        query_job.result()
        logger.info(f"Vector index `{index_name}` ensured on {full_table_id}.")
    except Exception as e:
        if "smaller than min allowed 5000" in str(e):
            logger.info(
                f"Table has < 5,000 rows ({full_table_id}). "
                f"BigQuery VECTOR_SEARCH will operate in exact brute-force cosine search mode with 100% recall."
            )
        else:
            raise e
