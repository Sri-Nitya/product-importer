from fastapi import APIRouter, File, UploadFile, HTTPException
from uuid import uuid4
from app.tasks.product_importer import import_products
import base64

router = APIRouter(prefix="/upload", tags=["upload"])
@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    contents = await file.read()
    file_id = str(uuid4())

    encoded = base64.b64encode(contents).decode("utf-8")
    import_products.delay(file_id, encoded)

    return {
        "message": "File uploaded successfully.",
        "file_id": file_id,
        "filename": file.filename, 
    }
