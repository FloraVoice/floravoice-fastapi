from uuid import UUID
from typing import Optional, Type, TypeVar
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from app.schemas.auth.common import Token, Account, AccountCreate, AccountLogin
from app.schemas.auth.user_schemas import UserCreate, UserLogin, User as UserSchema
from app.schemas.auth.admin_schemas import AdminLogin, Admin as AdminSchema
from app.repositories.user_repository import UserRepository
from app.repositories.admin_repository import AdminRepository
from app.dependancies.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.exceptions.auth_exceptions import AccountAlreadyExist, InvalidCredentials
from app.exceptions.common import DatabaseIntegrityError

T = TypeVar("T", bound=Account)


class AccountRepository(Protocol):
    @staticmethod
    async def select_by_email(db: AsyncSession, email: str) -> Optional[object]: ...

    @staticmethod
    async def select_by_username(db: AsyncSession, username: str) -> Optional[object]: ...

    @staticmethod
    async def select_by_id(db: AsyncSession, id: UUID) -> Optional[object]: ...

    @staticmethod
    async def insert(db: AsyncSession, obj_in: dict) -> object: ...


async def _register(
    account_data: AccountCreate,
    db: AsyncSession,
    repository: Type[AccountRepository],
    response_schema: Type[T],
) -> T:
    if await repository.select_by_email(db, account_data.email):
        raise AccountAlreadyExist(f"Account with email '{account_data.email}' already exists")

    if await repository.select_by_username(db, account_data.username):
        raise AccountAlreadyExist(f"Account with username '{account_data.username}' already exists")

    try:
        account_dict = account_data.model_dump(exclude={"password"})
        account_dict["hashed_password"] = hash_password(account_data.password)
        account = await repository.insert(db, account_dict)
        return response_schema.model_validate(account)

    except IntegrityError as e:
        original = e.orig
        if isinstance(original, UniqueViolationError):
            raise AccountAlreadyExist("Account with this email or username already exists")
        else:
            raise DatabaseIntegrityError(str(original))


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


async def register_user(user_data: UserCreate, db: AsyncSession) -> UserSchema:
    return await _register(user_data, db, UserRepository, UserSchema)


async def login_user(credentials: UserLogin, db: AsyncSession) -> Token:
    return await _login(credentials, db, UserRepository)


async def refresh_user_token(refresh_token: str, db: AsyncSession) -> Token:
    return await _refresh(refresh_token, db, UserRepository)


async def login_admin(credentials: AdminLogin, db: AsyncSession) -> Token:
    return await _login(credentials, db, AdminRepository)


async def refresh_admin_token(refresh_token: str, db: AsyncSession) -> Token:
    return await _refresh(refresh_token, db, AdminRepository)
