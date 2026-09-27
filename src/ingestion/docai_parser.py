"""Document AI Layout Parser module for asynchronous batch processing of SEC 10-K filings."""

import functools
import logging
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import documentai_v1 as documentai

from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def get_docai_client(location: str = settings.DOCUMENTAI_LOCATION) -> documentai.DocumentProcessorServiceClient:
    """Return a cached Document Processor Service client instance."""
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=opts)


def get_or_create_layout_parser(
    project_id: str = settings.PROJECT_ID,
    location: str = settings.DOCUMENTAI_LOCATION,
    display_name: str = "sec-filing-layout-parser",
) -> str:
    """Retrieve existing Layout Parser processor or create a new one idempotently.

    Args:
        project_id: GCP Project ID.
        location: Document AI location ('us' or 'eu').
        display_name: Human-readable display name for the processor.

    Returns:
        The processor ID (e.g. '1234567890abcdef').
    """
    client = get_docai_client(location)
    parent = client.common_location_path(project_id, location)

    logger.info(f"Checking existing processors in {parent}...")
    try:
        processors = client.list_processors(parent=parent)
        for p in processors:
            if p.type_ == "LAYOUT_PARSER_PROCESSOR" and p.display_name == display_name:
                processor_id = p.name.split("/")[-1]
                logger.info(f"Found existing Layout Parser processor: {processor_id} ({p.name})")
                return processor_id
    except GoogleAPICallError as e:
        logger.warning(f"Could not list processors: {e}")

    logger.info(f"Creating new LAYOUT_PARSER_PROCESSOR: {display_name} in {location}...")
    processor = client.create_processor(
        parent=parent,
        processor=documentai.Processor(
            display_name=display_name,
            type_="LAYOUT_PARSER_PROCESSOR",
        ),
    )
    processor_id = processor.name.split("/")[-1]
    logger.info(f"Created Layout Parser processor: {processor_id} ({processor.name})")
    return processor_id


def batch_process_filings(
    processor_id: str,
    project_id: str = settings.PROJECT_ID,
    location: str = settings.DOCUMENTAI_LOCATION,
    gcs_input_prefix: str | None = None,
    gcs_output_uri: str | None = None,
    chunk_size: int = settings.DOCUMENTAI_CHUNK_SIZE,
    wait_for_completion: bool = True,
    timeout_seconds: int = 3600,
) -> str:
    """Run asynchronous batch processing on SEC 10-K PDFs in GCS using Layout Parser.

    Args:
        processor_id: The Document AI processor ID.
        project_id: GCP Project ID.
        location: Document AI location ('us' or 'eu').
        gcs_input_prefix: GCS URI prefix for input PDFs (e.g. gs://bucket/raw_pdfs/).
        gcs_output_uri: GCS URI for parsed output (e.g. gs://bucket/parsed_output/).
        chunk_size: Target token/character chunk size.
        wait_for_completion: Whether to block until the long-running operation completes.
        timeout_seconds: Timeout for blocking operation wait.

    Returns:
        The operation name.
    """
    if gcs_input_prefix is None:
        gcs_input_prefix = f"gs://{settings.BUCKET_NAME}/{settings.RAW_PDF_PREFIX}"
    if gcs_output_uri is None:
        gcs_output_uri = f"gs://{settings.BUCKET_NAME}/{settings.PARSED_OUTPUT_PREFIX}"

    client = get_docai_client(location)
    resource_name = client.processor_path(project_id, location, processor_id)

    logger.info(f"Configuring batch processing for processor: {resource_name}")
    logger.info(f"Input GCS prefix: {gcs_input_prefix}")
    logger.info(f"Output GCS URI: {gcs_output_uri}")

    gcs_input = documentai.BatchDocumentsInputConfig(
        gcs_prefix=documentai.GcsPrefix(gcs_uri_prefix=gcs_input_prefix)
    )

    gcs_output = documentai.DocumentOutputConfig(
        gcs_output_config=documentai.DocumentOutputConfig.GcsOutputConfig(
            gcs_uri=gcs_output_uri,
            field_mask="chunkedDocument,documentLayout",
        )
    )

    process_options = documentai.ProcessOptions(
        layout_config=documentai.ProcessOptions.LayoutConfig(
            chunking_config=documentai.ProcessOptions.LayoutConfig.ChunkingConfig(
                chunk_size=chunk_size,
                include_ancestor_headings=True,
            )
        )
    )

    request = documentai.BatchProcessRequest(
        name=resource_name,
        input_documents=gcs_input,
        document_output_config=gcs_output,
        process_options=process_options,
    )

    logger.info("Submitting batch process request to Document AI...")
    operation = client.batch_process_documents(request=request)
    op_name = operation.operation.name
    logger.info(f"Batch process operation launched: {op_name}")

    if wait_for_completion:
        logger.info(f"Waiting for batch operation to complete (timeout: {timeout_seconds}s)...")
        operation.result(timeout=timeout_seconds)
        logger.info("Document AI batch processing completed successfully!")

    return op_name


if __name__ == "__main__":
    proc_id = get_or_create_layout_parser()
    print(f"PROCESSOR_ID={proc_id}")
