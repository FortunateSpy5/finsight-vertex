"""Execution script to embed extracted chunks via text-embedding-004 and load into BigQuery."""

import json
import logging
from pathlib import Path
from google.cloud import bigquery

from src.config import settings
from src.ingestion.chunk_extractor import ChunkRecord
from src.ingestion.embedder import embed_chunks
from src.ingestion.bq_loader import (
    create_chunks_table,
    create_vector_index,
    get_bq_client,
    upsert_chunks_to_bigquery,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    chunks_file = Path("data/parsed_chunks/chunks.jsonl")
    if not chunks_file.exists():
        logger.error(f"Chunks file {chunks_file} not found. Run chunk_extractor first.")
        return

    logger.info(f"Loading chunks from {chunks_file}...")
    chunks: list[ChunkRecord] = []
    with open(chunks_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line.strip()))

    logger.info(f"Loaded {len(chunks)} chunks for embedding.")

    # 1. Generate 768-dim embeddings using Vertex AI text-embedding-004
    logger.info("Generating embeddings via Vertex AI text-embedding-004...")
    embedded_chunks = embed_chunks(
        chunks=chunks,
        project_id=settings.PROJECT_ID,
        location=settings.LOCATION,
        model_name=settings.EMBEDDING_MODEL_NAME,
        batch_size=15,
    )
    logger.info(f"Generated embeddings for {len(embedded_chunks)} chunks.")

    # 2. Initialize BigQuery table
    client = get_bq_client(settings.PROJECT_ID)
    create_chunks_table(client, dataset_id=settings.BQ_DATASET, table_id=settings.BQ_CHUNKS_TABLE)

    # 3. Idempotently upsert chunks into BigQuery
    logger.info(f"Upserting {len(embedded_chunks)} embedded chunks into BigQuery...")
    loaded_count = upsert_chunks_to_bigquery(
        client=client,
        chunks=embedded_chunks,
        dataset_id=settings.BQ_DATASET,
        table_id=settings.BQ_CHUNKS_TABLE,
    )
    logger.info(f"Successfully upserted {loaded_count} chunks into BigQuery lakehouse.")

    # 4. Create vector index
    logger.info("Ensuring IVF cosine vector index on BigQuery table...")
    create_vector_index(
        client=client,
        dataset_id=settings.BQ_DATASET,
        table_id=settings.BQ_CHUNKS_TABLE,
    )
    logger.info("BigQuery vector store pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
