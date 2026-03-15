from uuid import UUID
from typing import Optional, Type, TypeVar
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from app.schemas.auth.common import Token, Account, AccountCreate, AccountLogin
from app.schemas.auth.user_schemas import UserCreate, User as UserSchema, UserLogin
from app.schemas.auth.admin_schemas import AdminCreate, Admin as AdminSchema, AdminLogin
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


async def _register_account(
    account_data: AccountCreate,
    db: AsyncSession,
    repository: Type[AccountRepository],
    response_schema: Type[T],
) -> T:
    existing_email = await repository.select_by_email(db, account_data.email)
    if existing_email:
        raise AccountAlreadyExist(f"Account with email '{account_data.email}' already exists")

    existing_username = await repository.select_by_username(db, account_data.username)
    if existing_username:
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


async def _login_account(
    credentials: AccountLogin,
    db: AsyncSession,
    repository: Type[AccountRepository],
) -> Token:
    account = await repository.select_by_email(db, credentials.email)

    if not account:
        raise InvalidCredentials("Invalid email or password")

    if not verify_password(credentials.password, str(account.hashed_password)):
        raise InvalidCredentials("Invalid email or password")

    access_token = create_access_token(UUID(str(account.id)))
    refresh_token = create_refresh_token(UUID(str(account.id)))

    return Token(access_token=access_token, refresh_token=refresh_token)


async def _refresh_account_token(
    refresh_token: str,
    db: AsyncSession,
    repository: Type[AccountRepository],
) -> Token:
    try:
        account_id = verify_token(refresh_token)
        account = await repository.select_by_id(db, UUID(account_id))

        if not account:
            raise InvalidCredentials("Invalid refresh token")

        new_access_token = create_access_token(UUID(str(account.id)))
        new_refresh_token = create_refresh_token(UUID(str(account.id)))

        return Token(access_token=new_access_token, refresh_token=new_refresh_token)
    except InvalidCredentials:
        raise
    except Exception:
        raise InvalidCredentials("Invalid refresh token")


# --- User ---

async def register_user(user_data: UserCreate, db: AsyncSession) -> UserSchema:
    return await _register_account(user_data, db, UserRepository, UserSchema)


async def login_user(credentials: UserLogin, db: AsyncSession) -> Token:
    return await _login_account(credentials, db, UserRepository)


async def refresh_user_token(refresh_token: str, db: AsyncSession) -> Token:
    return await _refresh_account_token(refresh_token, db, UserRepository)


# --- Admin ---

async def register_admin(admin_data: AdminCreate, db: AsyncSession) -> AdminSchema:
    return await _register_account(admin_data, db, AdminRepository, AdminSchema)


async def login_admin(credentials: AdminLogin, db: AsyncSession) -> Token:
    return await _login_account(credentials, db, AdminRepository)


async def refresh_admin_token(refresh_token: str, db: AsyncSession) -> Token:
    return await _refresh_account_token(refresh_token, db, AdminRepository)
