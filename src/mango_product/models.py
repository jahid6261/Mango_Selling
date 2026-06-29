from datetime import datetime
from sqlalchemy import BigInteger, Integer, Column, DateTime, String, DECIMAL, ForeignKey, Text, Boolean, Float, func
from sqlalchemy.orm import relationship
from src.utils.db import DBModel

class Category(DBModel):
    __tablename__ = "categories"
    
    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(150), unique=True, nullable=False)
    slug = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
   
    products = relationship("MangoProduct", back_populates="category", cascade="all, delete-orphan")


class MangoProduct(DBModel):
    __tablename__ = "mango_products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    slug = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Float, default=0.0)
    stock = Column(DECIMAL(10, 2), default=0.0)
    is_available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    orders = relationship(
        "Order",
        back_populates="product",
        cascade="all, delete-orphan"
    )

class Review(DBModel):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("mango_products.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    
    product = relationship("MangoProduct", back_populates="reviews")
   
    user = relationship("UserModel", back_populates="reviews")