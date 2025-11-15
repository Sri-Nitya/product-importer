from sqlalchemy import Column, Integer, String, Boolean, Text, Index, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=True)

    __table_args__ = (
        Index('ix_products_sku_lower', func.lower(sku), unique=True),
    )