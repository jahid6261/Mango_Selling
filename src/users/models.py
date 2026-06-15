
from sqlalchemy import Column,Integer,String,Boolean,DateTime,Enum,func
import enum
from src.utils.db import DBModel
from sqlalchemy.orm import relationship


class UserRole(enum.Enum):
    user='user'
    admin='admin'
    


class UserModel(DBModel):
    
    __tablename__ = 'users'
    id= Column(Integer,primary_key=True,index=True)
    
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True,index=True)
    password=Column(String,nullable=False)
    number=Column(String(15),unique=True,index=True)
    address=Column(String(255),nullable=True)
    role=Column(Enum(UserRole),default=UserRole.user)
    is_active = Column(Boolean, default=False)
    activation_token = Column(String, nullable=True)
    
    created_at=Column(DateTime(timezone=True),server_default=func.now()) 
    updated_at=Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())
    
    
    reviews = relationship("Review", back_populates="user")
    orders = relationship(
        "Order",
        back_populates="user"
    )
