"""Register Vertex AI text-embedding-004 as a BigQuery Remote Model."""

import logging
from google.cloud import bigquery
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def setup_remote_model() -> None:
    client = bigquery.Client(project=settings.PROJECT_ID)
    model_id = f"`{settings.PROJECT_ID}.{settings.BQ_DATASET}.{settings.BQ_REMOTE_MODEL_NAME}`"
    connection_id = f"`{settings.PROJECT_ID}.us.{settings.BQ_CONNECTION_ID}`"

    sql = f"""
    CREATE OR REPLACE MODEL {model_id}
    REMOTE WITH CONNECTION {connection_id}
    OPTIONS (ENDPOINT = '{settings.EMBEDDING_MODEL_NAME}');
    """
    logger.info(f"Creating Remote Model {model_id} via {connection_id}...")
    job = client.query(sql)
    job.result()
    logger.info("BigQuery Remote Embedding Model successfully registered!")

    # Verify model with test query
    test_sql = f"""
    SELECT * FROM ML.GENERATE_EMBEDDING(
        MODEL {model_id},
        (SELECT 'Testing remote embedding in BigQuery SQL' AS content),
        STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_QUERY' AS task_type)
    );
    """
    logger.info("Testing in-SQL embedding generation via ML.GENERATE_EMBEDDING...")
    test_job = client.query(test_sql)
    rows = list(test_job.result())
    logger.info(f"Test query succeeded! Returned {len(rows)} row with vector output.")


if __name__ == "__main__":
    setup_remote_model()
