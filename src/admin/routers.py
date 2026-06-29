

from fastapi import APIRouter,Depends,status

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import get_db

from src.admin.schemas import updateOrderstatusRequest

from src.admin.service import (
    get_all_orders,
    get_order_by_id,
    update_order_status
)



admin_routes=APIRouter(prefix='/admin',tags=["admin"])

@admin_routes.get('/orders',status_code=status.HTTP_200_OK)

async def all_orders(db:AsyncSession=Depends(get_db)):
    return await get_all_orders(db)


@admin_routes.get("orders/{order_id}",status_code=status.HTTP_200_OK)

async def  get_order_by_id(order_id:int,db:AsyncSession=Depends(get_db)):
    return await get_order_by_id(order_id,db)


@admin_routes.patch("/orders/{order_id}/",status_code=status.HTTP_200_OK)

async def update_order(order_id:int,request:updateOrderstatusRequest,db:AsyncSession=Depends(get_db)):

    return await update_order_status(order_id,request,db)