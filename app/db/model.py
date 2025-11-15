from sqlalchemy import Column, Integer, String, Boolean, Text, Index, func, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSON

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

class ImportJob(Base):
    __tablename__ = 'import_jobs'

    id = Column(String(36), primary_key=True)
    filename = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")
    progress = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    