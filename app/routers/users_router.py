from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.dependancies.auth import get_current_admin
from app.schemas.auth.user_schemas import User, UserCreate, UserUpdate
from app.services import user_service
from app.exceptions.auth_exceptions import AccountAlreadyExist, AccountNotFound
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(get_current_admin)])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.create_user(data, db)
    except AccountAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[User])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_service.get_all_users(db)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.get_user(user_id, db)
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user_id: UUID, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.update_user(user_id, data, db)
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.delete_user(user_id, db)
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
