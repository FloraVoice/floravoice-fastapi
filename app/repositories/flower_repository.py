from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.flower import Flower


class FlowerRepository:
    @staticmethod
    async def select_by_id(db: AsyncSession, id: UUID) -> Optional[Flower]:
        result = await db.execute(select(Flower).where(Flower.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_all(db: AsyncSession) -> List[Flower]:
        result = await db.execute(select(Flower))
        return list(result.scalars().all())

    @staticmethod
    async def insert(db: AsyncSession, obj_in: dict) -> Flower:
        flower = Flower(**obj_in)
        db.add(flower)
        await db.commit()
        await db.refresh(flower)
        return flower

    @staticmethod
    async def update(db: AsyncSession, db_obj: Flower, obj_in: dict) -> Flower:
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id: UUID) -> Optional[Flower]:
        result = await db.execute(select(Flower).where(Flower.id == id))
        flower = result.scalar_one_or_none()

        if flower:
            await db.delete(flower)
            await db.commit()

        return flower
