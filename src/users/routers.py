

from  fastapi import APIRouter,Depends,HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session 


from src.users.schemas import UserProfileResponse,LoginResponse,UserRegistrationRequest, UserLoginRequest
from src.users import services
from src.utils.db import get_db
from src.depends.auth_depends import require_user_id
from typing import Annotated
from src.users.models import UserModel
from sqlalchemy import select

users_routes=APIRouter(prefix="/users",tags=["Users"])



@users_routes.post("/register",response_model=UserProfileResponse)

async def register(request:UserRegistrationRequest, db: AsyncSession = Depends(get_db)):
    return await services.register(request,db)


@users_routes.get("/activate/{token}")
async def activate_account(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(
        select(UserModel).where(
            UserModel.activation_token == token
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid activation link"
        )

    if user.is_active:
        return {
            "message": "Account already activated"
        }

    user.is_active = True
    user.activation_token = None

    await db.commit()

    return {
        "message": "Account activated successfully"
    }

@users_routes.post("/login",response_model=LoginResponse)

async def login(request:UserLoginRequest, db: AsyncSession = Depends(get_db)):
    return await services.login(request,db)


@users_routes.get("/profile", response_model=UserProfileResponse)
async def profile(
    user=Depends(require_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await services.profile(user["user_id"], db)