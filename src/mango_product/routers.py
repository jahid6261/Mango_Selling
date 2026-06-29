
from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db import get_db
from src.mango_product import services
from src.mango_product.schemas import(CategoryResponse,CategoryRequest,CategoryUpdateRequest,CategoryBulkDeleteRequest,
                                      
                                      MangoProductRequest,
                                      MangoProductResponse,
                                      MangoProductDeleteBulkRequest,
                                      ReviewRequst,ReviewResponse


)
from typing import Optional 
from src.depends.admin_check import require_admin
from src.depends.auth_depends import require_user_id

                                        
mango_product_routes=APIRouter(prefix="/products",tags=['Products'])


@mango_product_routes.post('/category',response_model=CategoryResponse)
async def create_category(request:CategoryRequest,user=Depends(require_admin),db :AsyncSession=Depends(get_db)):
     return await services.create_category(request,db)




@mango_product_routes.get("/all-category",response_model=list[CategoryResponse])
async def all_category(db:AsyncSession=Depends(get_db)):
    return await services.all_category(db)




@mango_product_routes.get("/categories/{category_id}")
async def get_category_by_id(category_id:int,db:AsyncSession=Depends(get_db)):
    return await services.get_category_by_id(category_id,db)




@mango_product_routes.put("/categories/{category_id}")
async def update_category_route( category_id: int, request: CategoryUpdateRequest, user=Depends(require_admin), db: AsyncSession = Depends(get_db)):
    return await services.update_category(category_id, request, db)

  
   


@mango_product_routes.put("/update-category-bulk")

async def update_category_bulk(request:list[CategoryUpdateRequest],user=Depends(require_admin),db:AsyncSession=Depends(get_db)):
    return await services.update_category_bulk(request,db)



@mango_product_routes.delete("/categories/{category_id}")
async def category_delete(category_id:int,user=Depends(require_admin),db:AsyncSession=Depends(get_db)):
    return await services.category_delete(category_id,db)


@mango_product_routes.delete("/delete-category-bulk")

async def category_bulk_delete(request:CategoryBulkDeleteRequest,user=Depends(require_admin),db:AsyncSession=Depends(get_db)):
    return await services.category_bulk_delete(request,db)



# product cured routes

@mango_product_routes.post("/create-product",response_model=MangoProductResponse)

async def create_product(request:MangoProductRequest,user=Depends(require_admin),db:AsyncSession=Depends(get_db)):
    return await services.create_product(request,db)






@mango_product_routes.get("/search", response_model=list[MangoProductResponse])
async def search_products(
    product_id: Optional[int] = Query(None, description="নির্দিষ্ট আইডি দিয়ে সার্চ করুন"),
    search_name: Optional[str] = Query(None, description="প্রোডাক্টের নাম দিয়ে সার্চ করুন (Case-insensitive)"),
    min_price: Optional[float] = Query(None, description="সর্বনিম্ন প্রাইস ফিল্টার"),
    max_price: Optional[float] = Query(None, description="সর্বোচ্চ প্রাইস ফিল্টার"),
    db: AsyncSession = Depends(get_db)
):
    
    return await services.get_products_processed(
        db=db,
        product_id=product_id,
        search_name=search_name,
        min_price=min_price,
        max_price=max_price
    )


@mango_product_routes.get("/all-products",response_model=list[MangoProductResponse])

async def all_products(db:AsyncSession=Depends(get_db)):
    return await services.get_all_products(db)


@mango_product_routes.delete("/products-delete-bulk")
async def  product_delete_bulk(request:MangoProductDeleteBulkRequest,user=Depends(require_admin),db:AsyncSession=Depends(get_db)):
    return await services.product_delete_bulk(request,db)



@mango_product_routes.post("/product-review",response_model=ReviewResponse)

async def prodcut_review(request:ReviewRequst,
                         db:AsyncSession=Depends(get_db),
                         user=Depends(require_user_id)
                         ):
    

    return await services.create_review(
        request=request,
        user_id=user['user_id'],
        db=db
    )