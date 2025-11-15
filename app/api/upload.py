from fastapi import APIRouter, File, UploadFile, HTTPException
from uuid import uuid4
from app.tasks.product_importer import import_products
import os
from app.db.session import SessionLocal
from app.db.model import ImportJob

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "app/uploads"

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")

    with open(file_path, "wb") as f:
        while content := await file.read(1024*1024):
            f.write(content)
    import_products.delay(file_id, file_path, file.filename)

    return {
        "message": "File uploaded successfully.",
        "file_id": file_id,
        "filename": file.filename, 
        "path": file_path
    }

@router.get("/progress/{file_id}")
def check_progress(file_id: str):
    db = SessionLocal()
    job = db.query(ImportJob).filter(ImportJob.id == file_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="File ID not found.")
    
    return {
        "file_id": job.id,
        "filename": job.filename,
        "status": job.status,
        "progress": job.progress
    }
