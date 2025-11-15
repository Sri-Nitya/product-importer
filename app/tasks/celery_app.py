import os
from celery import Celery

redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "product_importer",
    broker=redis_url,
    backend=redis_url
)

celery_app.conf.update(
    task_routes={
        "app.tasks.product_importer.*": {"queue": "product_importer_queue"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

celery_app.autodiscover_tasks(['app.tasks'])

from app.tasks import product_importer 
