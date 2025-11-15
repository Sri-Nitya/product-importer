from app.tasks.celery_app import celery_app
import logging
import csv
from app.db.session import SessionLocal
from app.db.model import Product, ImportJob
from sqlalchemy import func

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.product_importer.import_products")
def import_products(file_id: str, file_path: str, filename: str):
    try:
        with SessionLocal() as db:
            job = ImportJob(id=file_id, filename=filename, status="processing", progress=0)
            db.add(job)
            db.commit()

        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            total = len(rows)

            with SessionLocal() as db:
                for idx, row in enumerate(rows, start=1):
                    sku = row["sku"].strip()

                    existing_product = (
                        db.query(Product)
                        .filter(func.lower(Product.sku) == sku.lower())
                        .first()
                    )

                    if existing_product:
                        existing_product.name = row["name"]
                        existing_product.description = row["description"]
                        existing_product.active = True
                    else:
                        product = Product(
                            sku=sku,
                            name=row["name"],
                            description=row["description"],
                            active=True
                        )
                        db.add(product)

                    if idx % 100 == 0 or idx == total:
                        job = db.query(ImportJob).filter_by(id=file_id).first()
                        if job:
                            job.progress = int(idx / total * 100)
                            db.commit()

                job = db.query(ImportJob).filter_by(id=file_id).first()
                if job:
                    job.status = "completed"
                    job.progress = 100
                    db.commit()

    except Exception as e:
        logger.error(f"Import error for file ID {file_id}: {e}")
        try:
            with SessionLocal() as db:
                job = db.query(ImportJob).filter_by(id=file_id).first()
                if job:
                    job.status = "failed"
                    db.commit()
        except Exception as inner_e:
            logger.error(f"Failed to update job status for file ID {file_id}: {inner_e}")
