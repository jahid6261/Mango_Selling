import enum

from sqlalchemy import Column, Integer, DECIMAL, func, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from src.utils.db import DBModel


class OrderStatus(str, enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'


class Order(DBModel):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('mango_products.id', ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
   
    

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

   
    user = relationship("UserModel", back_populates="orders")
    product = relationship("MangoProduct", back_populates="orders")

   

   

  

   

 