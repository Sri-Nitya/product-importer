from app.tasks.celery_app import celery_app
import logging
import csv
from app.db.session import SessionLocal
from app.db.model import Product
from sqlalchemy import func

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.product_importer.import_products")
def import_products(file_id: str, file_path: str):
    print(f"Importing products from file ID: {file_id}")
    logger.info(f"Importing products from file ID: {file_id}")

    db = SessionLocal()

    try:
        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                sku = row["sku"].strip()

                existing_product = (
                    db.query(Product)
                    .filter(func.lower(Product.sku) == sku.lower())
                    .first()
                )

                if existing_product:
                    existing_product.name = row.get("name", "")
                    existing_product.description = row.get("description", "")
                    existing_product.active = True
                    logger.info(f"Updated product SKU: {sku}")

                else:
                    product = Product(
                        sku=sku,
                        name=row.get("name", ""),
                        description=row.get("description", ""),
                        active=True, 
                    )
                    db.add(product)
                    logger.info(f"Created product SKU: {sku}")

            db.commit()
            logger.info(f"Successfully imported file ID: {file_id}")

    except Exception as e:
        db.rollback()
        logger.error(f"Import error for file ID {file_id}: {e}")
        return {"status": "error", "file_id": file_id}

    return {"status": "success", "file_id": file_id}
