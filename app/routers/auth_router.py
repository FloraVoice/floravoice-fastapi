from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.auth.common import Token, TokenRefresh
from app.schemas.auth.user_schemas import User, UserCreate, UserLogin
from app.services import auth_service
from app.exceptions.user_exc import UserAlreadyExists, InvalidCredentials
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await auth_service.register_user(data, db)
        return user

    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        token = await auth_service.login_user(credentials, db)
        return token

    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=Token)
async def refresh_token(token_data: TokenRefresh, db: AsyncSession = Depends(get_db)):
    try:
        token = await auth_service.refresh_access_token(token_data.refresh_token, db)
        return token

    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))