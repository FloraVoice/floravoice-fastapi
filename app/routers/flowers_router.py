from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.dependancies.auth import get_current_admin
from app.models.admin import Admin as AdminModel
from app.schemas.flowers.flower_schemas import FlowerCreate, FlowerUpdate, FlowerResponse
from app.services import flower_service
from app.exceptions.flower_exceptions import FlowerNotFound


router = APIRouter(prefix="/flowers", tags=["Flowers"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=FlowerResponse)
async def create_flower(
    data: FlowerCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminModel = Depends(get_current_admin),
):
    return await flower_service.create_flower(data, db)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[FlowerResponse])
async def get_all_flowers(
    db: AsyncSession = Depends(get_db),
    admin: AdminModel = Depends(get_current_admin),
):
    return await flower_service.get_all_flowers(db)


@router.get("/{flower_id}", status_code=status.HTTP_200_OK, response_model=FlowerResponse)
async def get_flower(
    flower_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: AdminModel = Depends(get_current_admin),
):
    try:
        return await flower_service.get_flower(flower_id, db)
    except FlowerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{flower_id}", status_code=status.HTTP_200_OK, response_model=FlowerResponse)
async def update_flower(
    flower_id: UUID,
    data: FlowerUpdate,
    db: AsyncSession = Depends(get_db),
    admin: AdminModel = Depends(get_current_admin),
):
    try:
        return await flower_service.update_flower(flower_id, data, db)
    except FlowerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{flower_id}", status_code=status.HTTP_200_OK, response_model=FlowerResponse)
async def delete_flower(
    flower_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: AdminModel = Depends(get_current_admin),
):
    try:
        return await flower_service.delete_flower(flower_id, db)
    except FlowerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
