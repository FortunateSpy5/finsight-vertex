"""Configuration settings for FinSight-Vertex enterprise pipeline."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    """Project-wide settings and resource identifiers."""

    # Google Cloud Project Configuration
    PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "divine-tempo-509920-t3")
    LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    DOCUMENTAI_LOCATION: str = os.getenv("DOCUMENTAI_LOCATION", "us")
    DOCUMENTAI_PROCESSOR_ID: str = os.getenv("DOCUMENTAI_PROCESSOR_ID", "a775315cd85516ac")

    # Cloud Storage Lakehouse
    BUCKET_NAME: str = os.getenv(
        "GCS_BUCKET_NAME", "finsight-document-lakehouse-divine-tempo"
    )
    RAW_PDF_PREFIX: str = "raw_pdfs/"
    PARSED_OUTPUT_PREFIX: str = "parsed_output/"
    STAGING_PREFIX: str = "staging/"

    # BigQuery Configuration
    BQ_DATASET: str = os.getenv("BQ_DATASET_NAME", "finsight_lakehouse")
    BQ_CHUNKS_TABLE: str = "financial_chunks"
    BQ_REMOTE_MODEL_NAME: str = "vertex_embed_model"
    BQ_CONNECTION_ID: str = "vertex_ai_conn"

    # Embedding & Reasoning Models
    EMBEDDING_MODEL_NAME: str = "text-embedding-004"
    EMBEDDING_DIMENSION: int = 768
    SUPERVISOR_MODEL_NAME: str = "gemini-2.0-flash"
    EVAL_JUDGE_MODEL_NAME: str = "gemini-1.5-flash"

    # Processing Constants
    DOCUMENTAI_CHUNK_SIZE: int = 1024


settings = Settings()
