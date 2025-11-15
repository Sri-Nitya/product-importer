from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from app.api.upload import router as upload_router
from app.api import products

app = FastAPI(title="Product Importer API")

app.include_router(products.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.get("/products")
def serve_products():
    return FileResponse("app/static/products.html")

app.include_router(upload_router)
