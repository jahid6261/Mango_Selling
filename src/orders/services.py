from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from src.orders.models import Order,OrderStatus
from src.orders.schemas import OrderRequest, OrderResponse
from src.mango_product.models import MangoProduct
from src.users.models import UserModel
import traceback

async def create_order(
    db: AsyncSession,
    user_id: int,
    request: OrderRequest
):

    # Check user
    result = await db.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check product
    result = await db.execute(
        select(MangoProduct).where(
            MangoProduct.id == request.product_id
        )
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Stock check
    quantity = Decimal(str(request.quantity))

    if product.stock < quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    total_price = product.price *  Decimal(str(request.quantity))

    new_order = Order(
        user_id=user_id,
        product_id=request.product_id,
        quantity=request.quantity,
        total_price=total_price
    )

    db.add(new_order)

    # Reduce stock
    product.stock -=  Decimal(str(request.quantity))

    try:
        await db.commit()
        await db.refresh(new_order)

    except Exception as e:
     await db.rollback()
     traceback.print_exc()
     raise HTTPException(
        status_code=500,
        detail=str(e)
    )
    return OrderResponse(
        id=new_order.id,
        user_id=new_order.user_id,
        product_id=new_order.product_id,
        quantity=new_order.quantity,
        total_price=float(new_order.total_price),
        status=new_order.status.value
    )



async def get_my_order(db: AsyncSession, user_id: int):

    result = await db.execute(
        select(UserModel).where(UserModel.id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    result = await db.execute(
        select(Order).where(Order.user_id == user_id)
    )

    orders = result.scalars().all()

    return [
        OrderResponse(
            id=order.id,
            user_id=order.user_id,
            product_id=order.product_id,
            quantity=order.quantity,
            total_price=float(order.total_price),
            status=order.status.value
        )
        for order in orders
    ]



async def get_order_by_id(db:AsyncSession,order_id:int,user_id:int):

    result =await db.execute(select(UserModel).
                             where(UserModel.id==user_id))
    user=result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404,detail='user not found')
    


    result=await db.execute(select(Order).where(Order.id==order_id,
                                                Order.user_id==user_id))
    
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=float(order.total_price),
        status=order.status.value
    )   



async def cancel_order(db:AsyncSession,order_id:int,user_id:int):

  
  result= await db.execute(select(UserModel).where(UserModel.id==user_id))

  user=result.scalar_one_or_none()

  if not user:
      raise HTTPException(status_code=404,detail="User not found")


  result=await db.execute(select(Order).where(Order.id==order_id,
                                              Order.user_id==user_id)
  )


  order=result.scalar_one_or_none()

  if not order:    
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
  

  if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled"
        )
  


   # find product
  result = await db.execute(
        select(MangoProduct).where(
            MangoProduct.id == order.product_id
        )
    )

  product = result.scalar_one_or_none()

  if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # restore stock
  product.stock += order.quantity

    # update order status
  order.status = OrderStatus.CANCELLED

  try:
        await db.commit()
        await db.refresh(order)

  except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to cancel order"
        )

  return {
        "message": "Order cancelled successfully",
        "order_id": order.id,
        "status": order.status.value
    }
 