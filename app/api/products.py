from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.model import Product
from app.schemas import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    return [
        {
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "description": p.description,
            "active": p.active
        } for p in products
    ]


@router.post("/")
def create_product(product: ProductCreate):
    db = SessionLocal()
    existing = db.query(Product).filter(Product.sku == product.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")

    new_product = Product(
        sku=product.sku,
        name=product.name,
        description=product.description,
        active=True
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"id": new_product.id}


@router.put("/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    db = SessionLocal()
    existing = db.query(Product).filter(Product.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.name is not None:
        existing.name = product.name
    if product.description is not None:
        existing.description = product.description
    if product.active is not None:
        existing.active = product.active
    
    db.commit()
    db.refresh(existing)
    return {
        "id": existing.id,
        "sku": existing.sku,
        "name": existing.name,
        "description": existing.description,
        "active": existing.active
    }


@router.delete("/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()
    existing = db.query(Product).filter(Product.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(existing)
    db.commit()
    return {"id": product_id}

@router.delete("/")
def bulk_delete():
    db = SessionLocal()
    deleted = db.query(Product).delete()
    db.commit()
    return {"detail": f"Deleted {deleted} products"}