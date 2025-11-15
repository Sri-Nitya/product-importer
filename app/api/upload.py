from fastapi import APIRouter, File, UploadFile, HTTPException
from uuid import uuid4
from app.tasks.product_importer import import_products
import os

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
    import_products.delay(file_id, file_path)

    return {
        "message": "File uploaded successfully.",
        "file_id": file_id,
        "filename": file.filename, 
        "path": file_path
    }
