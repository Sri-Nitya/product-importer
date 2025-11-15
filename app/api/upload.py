from fastapi import APIRouter, File, UploadFile, HTTPException
from uuid import uuid4

router = APIRouter(prefix="/upload", tags=["upload"])
@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    contents = await file.read()
    file_id = str(uuid4())


    return {
        "message": "File uploaded successfully.",
        "file_id": file_id,
        "filename": file.filename, 
    }
