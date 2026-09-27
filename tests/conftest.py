"""Pytest global fixtures for FinSight-Vertex test suite."""

import pytest
from src.ingestion.docai_parser import get_docai_client
from src.ingestion.chunk_extractor import get_storage_client
from src.ingestion.embedder import get_embedding_model
from src.ingestion.bq_loader import get_bq_client


@pytest.fixture(autouse=True)
def clear_caches() -> None:
    """Clear all lru_cache instances before and after each test."""
    get_docai_client.cache_clear()
    get_storage_client.cache_clear()
    get_embedding_model.cache_clear()
    get_bq_client.cache_clear()
    yield
    get_docai_client.cache_clear()
    get_storage_client.cache_clear()
    get_embedding_model.cache_clear()
    get_bq_client.cache_clear()
