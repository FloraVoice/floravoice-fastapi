from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


class UserRepository:
    @staticmethod
    async def select_by_id(db: AsyncSession, id: UUID) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_all(db: AsyncSession) -> List[User]:
        result = await db.execute(select(User))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_by_username(db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def insert(db: AsyncSession, obj_in: dict) -> User:
        user = User(**obj_in)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update(db: AsyncSession, db_obj: User, obj_in: dict) -> User:
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id: UUID) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if user:
            await db.delete(user)
            await db.commit()

        return user
