"""Unit tests for Vertex AI embedding batcher."""

from unittest.mock import MagicMock, patch
from google.api_core.exceptions import ServiceUnavailable
import pytest

from src.ingestion.embedder import embed_chunks
from src.ingestion.chunk_extractor import ChunkRecord


def test_embed_chunks_batching() -> None:
    """Verify that chunks are batched and receive 768-dim embeddings."""
    mock_chunks: list[ChunkRecord] = [
        {
            "chunk_id": f"c_{i}",
            "content": f"Financial disclosure text {i}",
            "source_document": "BRK_10K.pdf",
            "source_headers": [],
            "page_start": 1,
            "page_end": 1,
        }
        for i in range(5)
    ]

    mock_emb_values = [0.1] * 768
    mock_emb_obj = MagicMock()
    mock_emb_obj.values = mock_emb_values

    with patch("vertexai.init"), patch(
        "vertexai.language_models.TextEmbeddingModel.from_pretrained"
    ) as mock_from_pretrained:
        mock_model = MagicMock()
        mock_model.get_embeddings.return_value = [mock_emb_obj] * 5
        mock_from_pretrained.return_value = mock_model

        result = embed_chunks(
            chunks=mock_chunks,
            project_id="test-proj",
            location="us-central1",
            batch_size=5,
        )

        assert len(result) == 5
        for item in result:
            assert "embedding" in item
            assert len(item["embedding"]) == 768


def test_embed_chunks_retry_on_transient_failure() -> None:
    """Verify that transient API failures trigger retry and recover."""
    mock_chunks: list[ChunkRecord] = [
        {
            "chunk_id": "c_failover",
            "content": "Sample content",
            "source_document": "BRK_10K.pdf",
            "source_headers": [],
            "page_start": 1,
            "page_end": 1,
        }
    ]

    mock_emb_obj = MagicMock()
    mock_emb_obj.values = [0.2] * 768

    with patch("vertexai.init"), patch(
        "vertexai.language_models.TextEmbeddingModel.from_pretrained"
    ) as mock_from_pretrained, patch("time.sleep"):
        mock_model = MagicMock()
        # Fail on attempt 1, succeed on attempt 2
        mock_model.get_embeddings.side_effect = [
            ServiceUnavailable("Transient GCP unavailable error"),
            [mock_emb_obj],
        ]
        mock_from_pretrained.return_value = mock_model

        result = embed_chunks(
            chunks=mock_chunks,
            project_id="test-proj",
            location="us-central1",
            batch_size=1,
            max_retries=3,
        )

        assert len(result) == 1
        assert len(result[0]["embedding"]) == 768
        assert mock_model.get_embeddings.call_count == 2
