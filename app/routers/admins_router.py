from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.dependancies.auth import get_current_admin
from app.schemas.auth.admin_schemas import Admin, AdminCreate, AdminUpdate
from app.services import admin_service
from app.exceptions.auth_exceptions import AccountAlreadyExist, AccountNotFound
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/admins", tags=["Admins"], dependencies=[Depends(get_current_admin)])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Admin)
async def create_admin(data: AdminCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await admin_service.create_admin(data, db)
    except AccountAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Admin])
async def get_all_admins(db: AsyncSession = Depends(get_db)):
    return await admin_service.get_all_admins(db)


@router.get("/{admin_id}", status_code=status.HTTP_200_OK, response_model=Admin)
async def get_admin(admin_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await admin_service.get_admin(admin_id, db)
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{admin_id}", status_code=status.HTTP_200_OK, response_model=Admin)
async def update_admin(admin_id: UUID, data: AdminUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await admin_service.update_admin(admin_id, data, db)
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{admin_id}", status_code=status.HTTP_200_OK, response_model=Admin)
async def delete_admin(admin_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await admin_service.delete_admin(admin_id, db)
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
