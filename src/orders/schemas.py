

from pydantic import BaseModel
from typing import List ,Optional

from datetime import datetime
from decimal import Decimal


class OrderRequest(BaseModel):

    product_id:int
    quantity:float
   


class OrderResponse(BaseModel):
    id:int
    user_id:int
    product_id:int
    quantity:float
    total_price:float
    status:str
    

