from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from src.users.routers import users_routes
from src.mango_product.routers import mango_product_routes
from src.orders.routers import order_routes
from src.core.routes.email_routes import router as email_router
from src.seed.admin_seed import create_admin
from src.utils.db import DB_Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with DB_Session() as db:
        await create_admin(db)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_routes)
app.include_router(mango_product_routes)
app.include_router(order_routes)
app.include_router(email_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Application!"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )