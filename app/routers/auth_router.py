from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.auth.common import Token, TokenRefresh
from app.schemas.auth.user_schemas import User, UserCreate, UserLogin
from app.schemas.auth.admin_schemas import Admin, AdminCreate, AdminLogin
from app.services import auth_service
from app.exceptions.auth_exceptions import AccountAlreadyExist, InvalidCredentials
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- User ---

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await auth_service.register_user(data, db)

    except AccountAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        return await auth_service.login_user(credentials, db)

    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=Token)
async def refresh_token(token_data: TokenRefresh, db: AsyncSession = Depends(get_db)):
    try:
        return await auth_service.refresh_user_token(token_data.refresh_token, db)

    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


# --- Admin ---

@router.post("/admin/register", status_code=status.HTTP_201_CREATED, response_model=Admin)
async def admin_register(data: AdminCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await auth_service.register_admin(data, db)

    except AccountAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


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
