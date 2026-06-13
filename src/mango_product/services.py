

from sqlalchemy.ext.asyncio import AsyncSession
from src.mango_product.models import Category,MangoProduct,Review
from src.mango_product.schemas import( CategoryRequest,MangoProductRequest,CategoryResponse,CategoryUpdateRequest,
                                      MangoProductResponse,CategoryBulkDeleteRequest,MangoProductDeleteBulkRequest
                                      
)
from src.utils.db import DB_Session
from sqlalchemy import select,update,delete
from fastapi import HTTPException,status
from sqlalchemy import update, bindparam,or_, and_




async def create_category(request:CategoryRequest,db:AsyncSession):
    new_category=Category(
        title=request.title.strip(),
        slug=request.slug.strip(),
        description=request.description.strip()
        
    )

    db.add(new_category)

    try:
        await db.commit()
        await db.refresh(new_category)
    except Exception:
        await db.rollback()
        raise Exception("failed to create Category")

    return CategoryResponse(
        id=new_category.id,
        title=new_category.title,
        slug=new_category.slug,
        description=new_category.description
    )


async def all_category(db:AsyncSession):
    query=select(Category)
    result=await db.execute(query)
    return result.scalars().all()


# singale query 

async def get_category_by_id(category_id:int,db:AsyncSession):
    query=select(Category).where(Category.id==category_id)
    result=await db.execute(query)
    return result.scalars().first()




async def update_category(category_id: int, request: CategoryUpdateRequest, db: AsyncSession):

    await db.execute(
        update(Category)
        .where(Category.id == category_id)  
        .values(
            title=request.title.strip(),
            slug=request.slug.strip(),
            description=request.description.strip()
        )
    )
    

    await db.commit()
    
  
    return {"message": "Category updated successfully"}


async def update_category_bulk(request: list[CategoryUpdateRequest], db: AsyncSession):
  
    update_data = [p.model_dump(exclude_unset=True) for p in request]
    
    if not update_data:
        raise HTTPException(status_code=400, detail="কোন ডাটা পাঠানো হয়নি।")

    try:
        
        
        stmt = update(Category)
        
       
        await db.execute(stmt, update_data)
        
        
        await db.commit()
        
        return {
            "status": "success", 
            "message": f"সফলভাবে {len(update_data)}টি ক্যাটাগরি আপডেট করা হয়েছে।"
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bulk update ব্যর্থ হয়েছে: {str(e)}"
        )


async def category_delete(category_id:int,db:AsyncSession):
    query=delete(Category).where(Category.id == category_id)
    result=await db.execute(query)

    if result.rowcount==0:
        raise HTTPException(status_code=404,detail="category is not found")
    
    await db.commit()
    return {'message':"category is deleted succesfully"}





async def category_bulk_delete(request:CategoryBulkDeleteRequest,db:AsyncSession ):
    

    if not request.ids:
        raise HTTPException(
            status_code=400,
            detail="No ids provided"
        )

    query = delete(Category).where(
        Category.id.in_(request.ids)
    )

    result = await db.execute(query)

    await db.commit()

    return {
        "message": f"{result.rowcount} category deleted successfully"
    }




# all product crud opperations will be here


async def create_product(request:MangoProductRequest,db:AsyncSession):

    new_product=MangoProduct(
        title=request.title.strip(),
        slug=request.slug.strip(),
        description=request.description.strip(),
        price=request.price,
        quantity=request.quantity,
        stock=request.stock,
        is_available=request.is_available,
        image_url=request.image_url.strip() if request.image_url else None,
        category_id=request.category_id



    )

    db.add(new_product)
    try:
        await db.commit()
        await db.refresh(new_product)
    except Exception:
        await db.rollback()
        raise Exception ("failed to create product")
    return MangoProductResponse(

        id=new_product.id,
        title=new_product.title,
        slug=new_product.slug,
        description=new_product.description,
        price=new_product.price,
        quantity=new_product.quantity,
        stock=new_product.stock,
        is_available=new_product.is_available,
        image_url=new_product.image_url,
        category_id=new_product.category_id
    )



async def get_products_processed(
    db: AsyncSession, 
    product_id: int = None, 
    search_name: str = None, 
    min_price: float = None, 
    max_price: float = None
) -> list[MangoProduct]:
  
    query = select(MangoProduct)
    filters = []

  
    if product_id is not None:
        filters.append(MangoProduct.id == product_id)

   
    if search_name and search_name.strip():
        search_term = f"%{search_name.strip()}%"
        filters.append(MangoProduct.title.ilike(search_term))


    if min_price is not None:
        filters.append(MangoProduct.price >= min_price)

    if max_price is not None:
        filters.append(MangoProduct.price <= max_price)

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    products = result.scalars().all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="prodcut not found"
        )

    return products


async def get_all_products(db: AsyncSession):
    query = select(MangoProduct)
    result = await db.execute(query)
    return result.scalars().all()



async def product_delete_bulk(request:MangoProductDeleteBulkRequest,db:AsyncSession):
    if not request.ids:
        raise HTTPException(
            status_code=400,
            detail="No ids provied"
        )
    query=delete(MangoProduct).where(MangoProduct.id.in_(request.ids))
    result=await db.execute(query)
    await db.commit()

    return {"message":f"{result.rowcount} product deleted successfully"}