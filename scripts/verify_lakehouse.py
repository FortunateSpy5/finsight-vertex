"""Verify the BigQuery vector lakehouse contents and execute test VECTOR_SEARCH."""

import logging
from google.cloud import bigquery
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def verify_lakehouse() -> None:
    client = bigquery.Client(project=settings.PROJECT_ID)
    table_ref = f"`{settings.PROJECT_ID}.{settings.BQ_DATASET}.{settings.BQ_CHUNKS_TABLE}`"

    # 1. Row count, distinct documents, and embedding dimensions
    metrics_sql = f"""
    SELECT
        COUNT(*) AS total_chunks,
        COUNT(DISTINCT source_document) AS total_filings,
        ARRAY_LENGTH(ANY_VALUE(embedding)) AS vector_dimensions
    FROM {table_ref}
    """
    logger.info("Executing Lakehouse metrics query...")
    rows = list(client.query(metrics_sql).result())
    for r in rows:
        logger.info(f"Total Chunks: {r.total_chunks}")
        logger.info(f"Total Filings: {r.total_filings}")
        logger.info(f"Vector Dimensions: {r.vector_dimensions}")

    # 2. Per-document chunk breakdown
    breakdown_sql = f"""
    SELECT
        source_document,
        COUNT(*) AS chunk_count,
        MIN(page_start) AS min_page,
        MAX(page_end) AS max_page
    FROM {table_ref}
    GROUP BY source_document
    ORDER BY source_document
    """
    logger.info("\nPer-Filing Breakdown:")
    for r in client.query(breakdown_sql).result():
        logger.info(f"  - {r.source_document}: {r.chunk_count} chunks (pages {r.min_page} - {r.max_page})")

    # 3. Test VECTOR_SEARCH with user query
    test_query = "What is Berkshire Hathaway's insurance float and how has it grown?"
    logger.info(f"\nTesting BigQuery VECTOR_SEARCH with query: '{test_query}'...")

    vertexai.init(project=settings.PROJECT_ID, location=settings.LOCATION)
    embed_model = TextEmbeddingModel.from_pretrained(settings.EMBEDDING_MODEL_NAME)
    query_emb = embed_model.get_embeddings(
        [TextEmbeddingInput(text=test_query, task_type="RETRIEVAL_QUERY")],
        output_dimensionality=settings.EMBEDDING_DIMENSION,
    )[0].values

    search_sql = f"""
    SELECT
        base.chunk_id,
        base.source_document,
        base.page_start,
        base.page_end,
        LEFT(base.content, 250) AS content_preview,
        distance
    FROM VECTOR_SEARCH(
        TABLE {table_ref},
        'embedding',
        (SELECT @query_vec AS query_vec),
        query_column_to_search => 'query_vec',
        top_k => 3,
        distance_type => 'COSINE'
    )
    ORDER BY distance ASC
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("query_vec", "FLOAT64", query_emb),
        ]
    )

    search_rows = list(client.query(search_sql, job_config=job_config).result())
    logger.info(f"\nVECTOR_SEARCH Results (Top {len(search_rows)}):")
    for idx, r in enumerate(search_rows, 1):
        logger.info(
            f"  [{idx}] Doc: {r.source_document} | Pages: {r.page_start}-{r.page_end} | Distance: {r.distance:.4f}"
        )
        logger.info(f"      Preview: {r.content_preview.replace(chr(10), ' ')}...")


if __name__ == "__main__":
    verify_lakehouse()
