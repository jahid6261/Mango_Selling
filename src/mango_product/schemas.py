from decimal import Decimal

from pydantic import BaseModel,ConfigDict,Field

from typing import Optional
from datetime import datetime


class CategoryRequest(BaseModel):
    title:str
    slug:str
    description:str
class CategoryUpdateRequest(BaseModel):
    id:int
    title:str
    slug:str
    description:str   

class CategoryBulkDeleteRequest(BaseModel):
    ids:list[int]

class CategoryResponse(BaseModel):
    id:int
    title:str
    slug:str
    description:str
    

class MangoProductRequest(BaseModel):
    title: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=150)
    description: str
    price: Decimal 
    quantity: float = 0.0
    stock: Decimal = 0.0
    is_available: bool = True
    image_url: Optional[str] = None
    category_id: int

    
    class Config:
        from_attributes = True





class MangoProductResponse(BaseModel):
    id:int
    title:str
    slug:str
    description:str
    price:float
    quantity:float
    stock:float
    is_available:bool
    image_url:Optional[str]
    category_id:int


class MangoProductDeleteBulkRequest(BaseModel):
    ids:list[int]
   


class ReviewRequst(BaseModel):
    product_id:int
    user_id:int
    rating:int = Field(..., ge=1, le=5, description="rating must be between 1 and 5")
    comment:Optional[str]

class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    


        
            