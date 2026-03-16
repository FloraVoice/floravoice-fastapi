from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.dependancies.auth import get_current_admin, get_current_user
from app.models.admin import Admin as AdminModel
from app.models.user import User as UserModel
from app.schemas.orders.order_schemas import OrderCreate, OrderResponse
from app.services import order_service
from app.exceptions.order_exceptions import OrderNotFound, FlowerNotFoundInOrder
from app.exceptions.auth_exceptions import AccountNotFound


router = APIRouter(prefix="/orders", tags=["Orders"])


# Admin endpoints

@router.get("/admin/all", status_code=status.HTTP_200_OK, response_model=List[OrderResponse])
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    _: AdminModel = Depends(get_current_admin),
):
    return await order_service.get_all_orders(db)


@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: AdminModel = Depends(get_current_admin),
):
    try:
        return await order_service.get_order(order_id, db)
    except OrderNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/admin/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
async def delete_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: AdminModel = Depends(get_current_admin),
):
    try:
        return await order_service.delete_order(order_id, db)
    except OrderNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# User endpoints

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(get_current_user),
):
    try:
        return await order_service.create_order(data, db)
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except FlowerNotFoundInOrder as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/my", status_code=status.HTTP_200_OK, response_model=List[OrderResponse])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return await order_service.get_orders_for_user(user.id, db)
