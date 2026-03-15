from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.admin import Admin


class AdminRepository:
    @staticmethod
    async def select_by_id(db: AsyncSession, id: UUID) -> Optional[Admin]:
        result = await db.execute(select(Admin).where(Admin.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_all(db: AsyncSession) -> List[Admin]:
        result = await db.execute(select(Admin))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_email(db: AsyncSession, email: str) -> Optional[Admin]:
        result = await db.execute(select(Admin).where(Admin.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_by_username(db: AsyncSession, username: str) -> Optional[Admin]:
        result = await db.execute(select(Admin).where(Admin.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def insert(db: AsyncSession, obj_in: dict) -> Admin:
        admin = Admin(**obj_in)
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        return admin

    @staticmethod
    async def update(db: AsyncSession, db_obj: Admin, obj_in: dict) -> Admin:
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id: UUID) -> Optional[Admin]:
        result = await db.execute(select(Admin).where(Admin.id == id))
        admin = result.scalar_one_or_none()

        if admin:
            await db.delete(admin)
            await db.commit()

        return admin
