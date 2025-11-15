from fastapi import FastAPI
from app.api.upload import router as upload_router

app = FastAPI(title="Product Importer API")

@app.get("/")
def root():
    return {"message": "Welcome to the Product Importer API"}

app.include_router(upload_router)
