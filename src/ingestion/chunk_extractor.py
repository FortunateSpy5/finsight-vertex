"""Extract and structure chunks from Document AI parsed JSON outputs in GCS."""

import functools
import json
import logging
from pathlib import Path
import re
from typing import TypedDict
from google.cloud import storage

from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ChunkRecord(TypedDict):
    """Schema for extracted document chunks."""

    chunk_id: str
    content: str
    source_document: str
    source_headers: list[str]
    page_start: int
    page_end: int


class EmbeddedChunkRecord(ChunkRecord):
    """Schema for chunks with generated vector embeddings."""

    embedding: list[float]


@functools.lru_cache(maxsize=1)
def get_storage_client(project_id: str = settings.PROJECT_ID) -> storage.Client:
    """Return a cached Google Cloud Storage client instance."""
    return storage.Client(project=project_id)


def extract_chunks_from_gcs(
    bucket_name: str = settings.BUCKET_NAME,
    output_prefix: str = settings.PARSED_OUTPUT_PREFIX,
    local_save_path: str | None = "data/parsed_chunks/chunks.jsonl",
) -> list[ChunkRecord]:
    """Download Document AI batch output JSONs from GCS and parse into structured chunks.

    Preserves Markdown tables, ancestor headings, and exact page spans.

    Args:
        bucket_name: GCS bucket containing parsed JSON files.
        output_prefix: GCS prefix where Document AI wrote batch outputs.
        local_save_path: Optional local path to cache extracted chunks as JSONL.

    Returns:
        List of structured ChunkRecord dictionaries.
    """
    client = get_storage_client(settings.PROJECT_ID)
    bucket = client.bucket(bucket_name)

    logger.info(f"Listing Document AI output blobs in gs://{bucket_name}/{output_prefix}...")
    blobs = bucket.list_blobs(prefix=output_prefix)

    all_chunks: list[ChunkRecord] = []
    seen_chunk_ids: set[str] = set()
    json_count = 0

    for blob in blobs:
        if not blob.name.endswith(".json"):
            continue

        json_count += 1
        logger.info(f"Downloading and parsing blob: {blob.name}")
        content_text = blob.download_as_text()
        try:
            doc_data = json.loads(content_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from {blob.name}: {e}")
            continue

        # Extract source document name from Document AI blob name (e.g. BRK_10K_2022-0.json -> BRK_10K_2022.pdf)
        blob_filename = blob.name.split("/")[-1]
        source_doc = re.sub(r"-\d+\.json$", ".pdf", blob_filename)
        if not source_doc.endswith(".pdf"):
            source_uri = doc_data.get("uri", "")
            source_doc = source_uri.split("/")[-1] if source_uri else "unknown.pdf"

        chunked_doc = doc_data.get("chunkedDocument", {})
        chunks = chunked_doc.get("chunks", [])

        for idx, chunk in enumerate(chunks):
            raw_chunk_id = chunk.get("chunkId", f"chunk_{idx}")
            chunk_id = f"{source_doc}_{raw_chunk_id}"
            chunk_content = chunk.get("content", "").strip()

            if not chunk_content or chunk_id in seen_chunk_ids:
                continue

            seen_chunk_ids.add(chunk_id)

            page_span = chunk.get("pageSpan", {})
            page_start = page_span.get("pageStart", 1)
            page_end = page_span.get("pageEnd", page_start)

            # Extract ancestor headers if provided as strings
            headers: list[str] = []
            for block_id in chunk.get("sourceBlockIds", []):
                if isinstance(block_id, str):
                    headers.append(block_id)
                elif isinstance(block_id, dict) and "text" in block_id:
                    headers.append(block_id["text"])

            all_chunks.append({
                "chunk_id": chunk_id,
                "content": chunk_content,
                "source_document": source_doc,
                "source_headers": headers,
                "page_start": int(page_start),
                "page_end": int(page_end),
            })

    logger.info(f"Parsed {json_count} JSON blobs, extracted {len(all_chunks)} unique chunks.")

    # Save to local JSONL for verification and offline inspection
    if local_save_path and all_chunks:
        save_file = Path(local_save_path)
        save_file.parent.mkdir(parents=True, exist_ok=True)
        with open(save_file, "w", encoding="utf-8") as f:
            for item in all_chunks:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        logger.info(f"Saved {len(all_chunks)} chunks to {save_file}")

    return all_chunks


if __name__ == "__main__":
    chunks = extract_chunks_from_gcs()
    print(f"Total extracted chunks: {len(chunks)}")
