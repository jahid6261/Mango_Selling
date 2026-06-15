
from src.users.models import UserModel,UserRole
from src.users.schemas import UserRegistrationRequest,UserLoginRequest,UserProfileResponse,LoginResponse

from sqlalchemy import select
from fastapi import  HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.security import hash_password,verify_password,encode_access_token
from src.utils.actvation_token import generate_activation_token
from src.core.services.email_service import send_email_service
from src.utils.settings import Settings



async def register(request: UserRegistrationRequest, db: AsyncSession):

    # 1. Check existing email
    email_query = await db.execute(
        select(UserModel).filter(UserModel.email == request.email.strip())
    )
    existing_email = email_query.scalars().first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    # 2. Generate token
    token = generate_activation_token()

    # 3. Create user
    new_user = UserModel(
        first_name=request.first_name.strip(),
        last_name=request.last_name.strip(),
        email=request.email.lower().strip(),
        number=request.number.strip(),
        password=hash_password(request.password),
        address=request.address.strip(),
        role=UserRole.user,

        is_active=False,
        activation_token=token
    )

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    # 4. Activation link
    activation_link = f"{Settings.BASE_URL}/users/activate/{token}"

    # 5. Send email via Celery
    send_email_service.delay(
        new_user.email,
        "Activate your account ",
        activation_link
    )

    # 6. Response
    return UserProfileResponse(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        role=new_user.role,
        number=new_user.number,
        address=new_user.address,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
        is_active=new_user.is_active
    )




     
                       
 
      
       
    

    

async def login(request: UserLoginRequest, db: AsyncSession):
  
    email = request.email.lower().strip()
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()

    if user is not None and verify_password(request.password, user.password):
        return LoginResponse(
            access_token=encode_access_token(
                user.id,
                user.email,
                user.role.value
               
            )
        )

   
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"}
    )




async def profile(user_id: int, db: AsyncSession):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if user is not None:
        return UserProfileResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            number=user.number,
            role=user.role,                
            address=user.address,   
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
     
   
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="User not found"
    )
 
