from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.auth.common import Token, TokenRefresh
from app.schemas.auth.admin_schemas import AdminLogin
from app.services import auth_service
from app.exceptions.auth_exceptions import InvalidCredentials


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/admin/login", status_code=status.HTTP_200_OK, response_model=Token)
async def admin_login(credentials: AdminLogin, db: AsyncSession = Depends(get_db)):
    try:
        return await auth_service.login_admin(credentials, db)

    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/admin/refresh", status_code=status.HTTP_200_OK, response_model=Token)
async def admin_refresh_token(token_data: TokenRefresh, db: AsyncSession = Depends(get_db)):
    try:
        return await auth_service.refresh_admin_token(token_data.refresh_token, db)

    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
