from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.users.models import UserModel, UserRole
from src.utils.security import hash_password
from src.utils.settings import settings


async def create_admin(db: AsyncSession):
    try:
        result = await db.execute(
            select(UserModel).where(
                UserModel.email == settings.ADMIN_EMAIL
            )
        )

        existing = result.scalar_one_or_none()

        if existing:
            print("Admin already exists. Skipping...")
            return

        admin = UserModel(
            first_name="Super",
            last_name="Admin",
            email=settings.ADMIN_EMAIL,
            password=hash_password(settings.ADMIN_PASSWORD),
            number="0000000000",
            address="Admin ctg",
            role=UserRole.admin
        )

        db.add(admin)
        await db.commit()
        await db.refresh(admin)

        print("Super Admin created successfully!")

    except Exception as e:
        await db.rollback()
        print(f"Error during admin seeding: {e}")
        raise