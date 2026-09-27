"""Unit tests for Document AI ingestion, chunk extraction, and BigQuery loader."""

import json
from unittest.mock import MagicMock, patch
import pytest

from src.ingestion.docai_parser import batch_process_filings, get_or_create_layout_parser
from src.ingestion.chunk_extractor import extract_chunks_from_gcs, ChunkRecord, EmbeddedChunkRecord
from src.ingestion.bq_loader import (
    create_chunks_table,
    create_vector_index,
    load_chunks_to_bigquery,
    upsert_chunks_to_bigquery,
    validate_identifier,
)


def test_validate_identifier() -> None:
    """Verify identifier validation blocks DDL injection."""
    assert validate_identifier("valid_table_123") == "valid_table_123"
    with pytest.raises(ValueError):
        validate_identifier("table; DROP TABLE users; --")
    with pytest.raises(ValueError):
        validate_identifier("table with spaces")


def test_get_or_create_layout_parser_existing() -> None:
    """Verify that an existing processor is discovered idempotently."""
    mock_processor = MagicMock()
    mock_processor.type_ = "LAYOUT_PARSER_PROCESSOR"
    mock_processor.display_name = "sec-filing-layout-parser"
    mock_processor.name = "projects/test-proj/locations/us/processors/test-proc-123"

    with patch("google.cloud.documentai_v1.DocumentProcessorServiceClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.common_location_path.return_value = "projects/test-proj/locations/us"
        mock_client.list_processors.return_value = [mock_processor]
        mock_client_cls.return_value = mock_client

        proc_id = get_or_create_layout_parser(
            project_id="test-proj",
            location="us",
            display_name="sec-filing-layout-parser",
        )
        assert proc_id == "test-proc-123"


def test_batch_process_filings() -> None:
    """Verify async batch dispatching with layout config and ancestor headings."""
    with patch("google.cloud.documentai_v1.DocumentProcessorServiceClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.processor_path.return_value = "projects/test-proj/locations/us/processors/test-proc"
        mock_operation = MagicMock()
        mock_operation.operation.name = "operations/op-12345"
        mock_client.batch_process_documents.return_value = mock_operation
        mock_client_cls.return_value = mock_client

        op_name = batch_process_filings(
            processor_id="test-proc",
            project_id="test-proj",
            location="us",
            gcs_input_prefix="gs://test-bucket/raw_pdfs/",
            gcs_output_uri="gs://test-bucket/parsed_output/",
            wait_for_completion=False,
        )

        assert op_name == "operations/op-12345"
        mock_client.batch_process_documents.assert_called_once()


def test_extract_chunks_from_gcs() -> None:
    """Verify chunk extraction from Document AI JSON format with table preservation."""
    fake_doc_json = {
        "uri": "gs://test-bucket/raw_pdfs/BRK_10K_2024.pdf",
        "chunkedDocument": {
            "chunks": [
                {
                    "chunkId": "chunk-001",
                    "content": "| Year | Revenue | Net Income |\n| 2024 | $371.4B | $96.2B |",
                    "pageSpan": {"pageStart": 42, "pageEnd": 42},
                    "sourceBlockIds": ["Item 7. Management Discussion"],
                }
            ]
        },
    }

    mock_blob = MagicMock()
    mock_blob.name = "parsed_output/op-123/BRK_10K_2024.pdf/0/output.json"
    mock_blob.download_as_text.return_value = json.dumps(fake_doc_json)

    with patch("google.cloud.storage.Client") as mock_storage_cls:
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_bucket.list_blobs.return_value = [mock_blob]
        mock_client.bucket.return_value = mock_bucket
        mock_storage_cls.return_value = mock_client

        chunks = extract_chunks_from_gcs(
            bucket_name="test-bucket",
            output_prefix="parsed_output/",
            local_save_path=None,
        )

        assert len(chunks) == 1
        assert chunks[0]["chunk_id"] == "BRK_10K_2024.pdf_chunk-001"
        assert "| Year | Revenue |" in chunks[0]["content"]
        assert chunks[0]["page_start"] == 42
        assert chunks[0]["source_document"] == "BRK_10K_2024.pdf"


def test_load_chunks_to_bigquery() -> None:
    """Verify batch NDJSON load job execution and cleanup."""
    mock_chunks: list[EmbeddedChunkRecord] = [
        {
            "chunk_id": "c1",
            "content": "Test content",
            "source_document": "BRK_10K_2024.pdf",
            "source_headers": [],
            "page_start": 1,
            "page_end": 1,
            "embedding": [0.1] * 768,
        }
    ]

    mock_client = MagicMock()
    mock_client.project = "test-proj"
    mock_job = MagicMock()
    mock_job.output_rows = 1
    mock_client.load_table_from_file.return_value = mock_job

    loaded = load_chunks_to_bigquery(
        mock_client,
        mock_chunks,
        dataset_id="test_ds",
        table_id="test_tbl",
    )
    assert loaded == 1
    mock_client.load_table_from_file.assert_called_once()


def test_create_vector_index() -> None:
    """Verify vector index creation SQL generation."""
    mock_client = MagicMock()
    mock_client.project = "test-proj"
    mock_query_job = MagicMock()
    mock_client.query.return_value = mock_query_job

    create_vector_index(
        mock_client,
        dataset_id="test_ds",
        table_id="test_tbl",
        index_name="test_idx",
    )
    mock_client.query.assert_called_once()
    sql_called = mock_client.query.call_args[0][0]
    assert "CREATE VECTOR INDEX IF NOT EXISTS `test_idx`" in sql_called
    assert "IVF" in sql_called
    assert "COSINE" in sql_called
