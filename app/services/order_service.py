from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.orders.order_schemas import OrderCreate, OrderResponse
from app.repositories.order_repository import OrderRepository
from app.repositories.flower_repository import FlowerRepository
from app.repositories.user_repository import UserRepository
from app.exceptions.order_exceptions import OrderNotFound, FlowerNotFoundInOrder
from app.exceptions.auth_exceptions import AccountNotFound


async def create_order(data: OrderCreate, db: AsyncSession) -> OrderResponse:
    user = await UserRepository.select_by_id(db, data.user_id)
    if not user:
        raise AccountNotFound(f"User with id '{data.user_id}' not found")

    items_data = []
    for item in data.items:
        flower = await FlowerRepository.select_by_id(db, item.flower_id)
        if not flower:
            raise FlowerNotFoundInOrder(f"Flower with id '{item.flower_id}' not found")
        items_data.append({
            "flower_id": item.flower_id,
            "quantity": item.quantity,
            "price_at_purchase": flower.price,
        })

    order = await OrderRepository.insert(db, {"user_id": data.user_id}, items_data)
    return OrderResponse.model_validate(order)


async def get_order(order_id: UUID, db: AsyncSession) -> OrderResponse:
    order = await OrderRepository.select_by_id(db, order_id)
    if not order:
        raise OrderNotFound(f"Order '{order_id}' not found")
    return OrderResponse.model_validate(order)


async def get_all_orders(db: AsyncSession) -> List[OrderResponse]:
    return [OrderResponse.model_validate(o) for o in await OrderRepository.select_all(db)]


async def get_orders_for_user(user_id: UUID, db: AsyncSession) -> List[OrderResponse]:
    return [OrderResponse.model_validate(o) for o in await OrderRepository.select_by_user_id(db, user_id)]


async def delete_order(order_id: UUID, db: AsyncSession) -> OrderResponse:
    order = await OrderRepository.delete(db, order_id)
    if not order:
        raise OrderNotFound(f"Order '{order_id}' not found")
    return OrderResponse.model_validate(order)
