"""Vertex AI text-embedding-004 batch embedding generator for financial chunks."""

import functools
import logging
import time
from google.api_core.exceptions import GoogleAPICallError
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

from src.config import settings
from src.ingestion.chunk_extractor import ChunkRecord, EmbeddedChunkRecord

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def get_embedding_model(
    project_id: str = settings.PROJECT_ID,
    location: str = settings.LOCATION,
    model_name: str = settings.EMBEDDING_MODEL_NAME,
) -> TextEmbeddingModel:
    """Initialize Vertex AI and return a cached TextEmbeddingModel instance."""
    logger.info(f"Initializing Vertex AI ({project_id}, {location}) with model {model_name}...")
    vertexai.init(project=project_id, location=location)
    return TextEmbeddingModel.from_pretrained(model_name)


def embed_chunks(
    chunks: list[ChunkRecord],
    project_id: str = settings.PROJECT_ID,
    location: str = settings.LOCATION,
    model_name: str = settings.EMBEDDING_MODEL_NAME,
    batch_size: int = 15,
    max_retries: int = 3,
) -> list[EmbeddedChunkRecord]:
    """Generate 768-dimensional embeddings for chunks using Vertex AI text-embedding-004.

    Batches in groups of 15 chunks (max 20,000 tokens per API call) to preserve Markdown tables.

    Args:
        chunks: List of chunk records with 'content' and 'source_document'.
        project_id: GCP project ID.
        location: Vertex AI location (e.g. us-central1).
        model_name: Model identifier (text-embedding-004).
        batch_size: Chunks per API request (safe default 15).
        max_retries: Retry attempts per batch.

    Returns:
        List of chunks with 'embedding' field populated.
    """
    model = get_embedding_model(project_id, location, model_name)
    total_chunks = len(chunks)
    logger.info(f"Embedding {total_chunks} chunks using {model_name} (batch_size={batch_size})...")

    embedded_chunks: list[EmbeddedChunkRecord] = []

    for i in range(0, total_chunks, batch_size):
        batch = chunks[i : i + batch_size]
        # Keep text within token boundaries (up to 6000 chars per chunk)
        batch_inputs = [
            TextEmbeddingInput(
                text=c["content"][:6000],
                task_type="RETRIEVAL_DOCUMENT",
                title=c.get("source_document", ""),
            )
            for c in batch
        ]

        batch_result: list[EmbeddedChunkRecord] = []
        for attempt in range(1, max_retries + 1):
            try:
                embeddings = model.get_embeddings(
                    batch_inputs,
                    output_dimensionality=settings.EMBEDDING_DIMENSION,
                )
                for chunk, emb in zip(batch, embeddings):
                    embedded_chunk: EmbeddedChunkRecord = {
                        "chunk_id": chunk["chunk_id"],
                        "content": chunk["content"],
                        "source_document": chunk["source_document"],
                        "source_headers": chunk["source_headers"],
                        "page_start": chunk["page_start"],
                        "page_end": chunk["page_end"],
                        "embedding": list(emb.values),
                    }
                    batch_result.append(embedded_chunk)
                break
            except (GoogleAPICallError, ConnectionError, TimeoutError, Exception) as e:
                logger.warning(f"Batch embedding attempt {attempt} failed: {e}")
                if attempt == max_retries:
                    logger.error(f"Exhausted retries for batch {i}..{i + len(batch)}")
                    raise e
                time.sleep(2**attempt)

        embedded_chunks.extend(batch_result)
        logger.info(
            f"Embedded batch {i // batch_size + 1}/{(total_chunks + batch_size - 1) // batch_size} "
            f"({len(embedded_chunks)}/{total_chunks})"
        )

    logger.info(f"Successfully generated embeddings for {len(embedded_chunks)} chunks.")
    return embedded_chunks
