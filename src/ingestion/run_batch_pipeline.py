"""Execution script to launch and monitor the Document AI Layout Parser batch ETL job."""

import logging
import sys
import time
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai

from src.config import settings
from src.ingestion.docai_parser import batch_process_filings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def launch_batch_job(wait: bool = False) -> str:
    """Launch Document AI Layout Parser batch extraction on GCS PDFs."""
    processor_id = settings.DOCUMENTAI_PROCESSOR_ID
    logger.info(f"Using Processor ID: {processor_id}")
    logger.info(f"Target Bucket: gs://{settings.BUCKET_NAME}/{settings.RAW_PDF_PREFIX}")
    logger.info(f"Output Destination: gs://{settings.BUCKET_NAME}/{settings.PARSED_OUTPUT_PREFIX}")

    op_name = batch_process_filings(
        processor_id=processor_id,
        project_id=settings.PROJECT_ID,
        location=settings.DOCUMENTAI_LOCATION,
        wait_for_completion=wait,
    )
    logger.info(f"Batch processing operation name: {op_name}")
    return op_name


def check_operation_status(operation_name: str) -> bool:
    """Check the status of a running Document AI operation."""
    opts = ClientOptions(api_endpoint=f"{settings.DOCUMENTAI_LOCATION}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    operations_client = client.transport.operations_client
    op = operations_client.get_operation(operation_name)
    logger.info(f"Operation done: {op.done}")
    if op.error.code:
        logger.error(f"Operation error: {op.error.message}")
    return op.done


if __name__ == "__main__":
    wait_flag = "--wait" in sys.argv
    op = launch_batch_job(wait=wait_flag)
    print(f"OPERATION_NAME={op}")
