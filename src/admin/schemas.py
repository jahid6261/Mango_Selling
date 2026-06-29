

from pydantic import BaseModel

from src.orders.models import OrderStatus


class updateOrderstatusRequest(BaseModel):
    status:OrderStatus