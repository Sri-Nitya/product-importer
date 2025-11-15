from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.product_importer.import_products")
def import_products(file_id: str, encoded: str):
    print(f"Importing products from file ID: {file_id}")
    logger.info(f"Importing products from file ID: {file_id}")

    return {"status": "success", "file_id": file_id}