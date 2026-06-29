

from fastapi import HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.orders.models import Order
from src.admin.schemas import updateOrderstatusRequest


async def get_all_orders(db: AsyncSession):
    result=await db.execute(select(Order))
    return result.scalars().all()


async def get_order_by_id(order_id:int,db:AsyncSession):
    result =await db.execute(
        select(Order).where(Order.id==order_id)
    )
    order=result.scalars().first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="order not found"
        )
    
    return order


async def update_order_status(order_id:int, request:updateOrderstatusRequest,db:AsyncSession):


    result= await db.execute( select(Order).where(Order.id==order_id)
                             
    )
     
    order = result.scalars().first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    

    order.status=request.status
    await db.commit()
    await db.refresh(order)

    return {
    "success": True,
    "message": "Order status updated successfully",
    'data':order
    
}

        

        
        
       

    
   
