from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.flowers.flower_schemas import FlowerCreate, FlowerUpdate, FlowerResponse
from app.repositories.flower_repository import FlowerRepository
from app.exceptions.flower_exceptions import FlowerNotFound


async def create_flower(data: FlowerCreate, db: AsyncSession) -> FlowerResponse:
    flower = await FlowerRepository.insert(db, data.model_dump())
    return FlowerResponse.model_validate(flower)


async def get_flower(flower_id: UUID, db: AsyncSession) -> FlowerResponse:
    flower = await FlowerRepository.select_by_id(db, flower_id)
    if not flower:
        raise FlowerNotFound(f"Flower with id '{flower_id}' not found")
    return FlowerResponse.model_validate(flower)


async def get_all_flowers(db: AsyncSession) -> List[FlowerResponse]:
    flowers = await FlowerRepository.select_all(db)
    return [FlowerResponse.model_validate(f) for f in flowers]


async def update_flower(flower_id: UUID, data: FlowerUpdate, db: AsyncSession) -> FlowerResponse:
    flower = await FlowerRepository.select_by_id(db, flower_id)
    if not flower:
        raise FlowerNotFound(f"Flower with id '{flower_id}' not found")
    updated = await FlowerRepository.update(db, flower, data.model_dump())
    return FlowerResponse.model_validate(updated)


async def delete_flower(flower_id: UUID, db: AsyncSession) -> FlowerResponse:
    flower = await FlowerRepository.delete(db, flower_id)
    if not flower:
        raise FlowerNotFound(f"Flower with id '{flower_id}' not found")
    return FlowerResponse.model_validate(flower)
