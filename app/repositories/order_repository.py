from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.order import Order, OrderItem


class OrderRepository:
    @staticmethod
    async def select_by_id(db: AsyncSession, order_id: UUID) -> Optional[Order]:
        result = await db.execute(select(Order).where(Order.id == order_id).options(selectinload(Order.items)))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_all(db: AsyncSession) -> List[Order]:
        result = await db.execute(select(Order).options(selectinload(Order.items)))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_user_id(db: AsyncSession, user_id: UUID) -> List[Order]:
        result = await db.execute(select(Order).where(Order.user_id == user_id).options(selectinload(Order.items)))
        return list(result.scalars().all())

    @staticmethod
    async def insert(db: AsyncSession, order_data: dict, items_data: List[dict]) -> Order:
        order = Order(**order_data)
        db.add(order)
        await db.flush()          # assigns order.id without committing
        for item_dict in items_data:
            db.add(OrderItem(order_id=order.id, **item_dict))
        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def delete(db: AsyncSession, order_id: UUID) -> Optional[Order]:
        result = await db.execute(select(Order).where(Order.id == order_id).options(selectinload(Order.items)))
        order = result.scalar_one_or_none()
        if order:
            await db.delete(order)
            await db.commit()
        return order
