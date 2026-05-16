from uuid import UUID
from typing import Optional, Type
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth.common import Token, AccountLogin
from app.schemas.auth.admin_schemas import AdminLogin
from app.repositories.admin_repository import AdminRepository
from app.dependancies.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.exceptions.auth_exceptions import InvalidCredentials


class AccountRepository(Protocol):
    @staticmethod
    async def select_by_email(db: AsyncSession, email: str) -> Optional[object]: ...

    @staticmethod
    async def select_by_id(db: AsyncSession, id: UUID) -> Optional[object]: ...


async def _login(
    credentials: AccountLogin,
    db: AsyncSession,
    repository: Type[AccountRepository],
) -> Token:
    account = await repository.select_by_email(db, credentials.email)

    if not account or not verify_password(credentials.password, str(account.hashed_password)):
        raise InvalidCredentials("Invalid email or password")

    return Token(
        access_token=create_access_token(UUID(str(account.id))),
        refresh_token=create_refresh_token(UUID(str(account.id))),
    )


async def _refresh(
    refresh_token: str,
    db: AsyncSession,
    repository: Type[AccountRepository],
) -> Token:
    try:
        account_id = verify_token(refresh_token)
        account = await repository.select_by_id(db, UUID(account_id))

        if not account:
            raise InvalidCredentials("Invalid refresh token")

        return Token(
            access_token=create_access_token(UUID(str(account.id))),
            refresh_token=create_refresh_token(UUID(str(account.id))),
        )
    except InvalidCredentials:
        raise
    except Exception:
        raise InvalidCredentials("Invalid refresh token")


async def login_admin(credentials: AdminLogin, db: AsyncSession) -> Token:
    return await _login(credentials, db, AdminRepository)


async def refresh_admin_token(refresh_token: str, db: AsyncSession) -> Token:
    return await _refresh(refresh_token, db, AdminRepository)
