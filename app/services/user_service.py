from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from app.schemas.auth.user_schemas import UserCreate, UserUpdate, User as UserSchema
from app.repositories.user_repository import UserRepository
from app.dependancies.auth import hash_password
from app.exceptions.auth_exceptions import AccountAlreadyExist, AccountNotFound
from app.exceptions.common import DatabaseIntegrityError


async def create_user(user_data: UserCreate, db: AsyncSession) -> UserSchema:
    if await UserRepository.select_by_email(db, user_data.email):
        raise AccountAlreadyExist(f"Account with email '{user_data.email}' already exists")

    if await UserRepository.select_by_username(db, user_data.username):
        raise AccountAlreadyExist(f"Account with username '{user_data.username}' already exists")

    try:
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hash_password(user_data.password)
        user = await UserRepository.insert(db, user_dict)
        return UserSchema.model_validate(user)

    except IntegrityError as e:
        original = e.orig
        if isinstance(original, UniqueViolationError):
            raise AccountAlreadyExist("Account with this email or username already exists")
        else:
            raise DatabaseIntegrityError(str(original))


async def get_all_users(db: AsyncSession) -> list[UserSchema]:
    users = await UserRepository.select_all(db)
    return [UserSchema.model_validate(u) for u in users]


async def get_user(user_id: UUID, db: AsyncSession) -> UserSchema:
    user = await UserRepository.select_by_id(db, user_id)
    if not user:
        raise AccountNotFound("User not found")
    return UserSchema.model_validate(user)


async def update_user(user_id: UUID, user_data: UserUpdate, db: AsyncSession) -> UserSchema:
    user = await UserRepository.select_by_id(db, user_id)
    if not user:
        raise AccountNotFound("User not found")

    update_dict = user_data.model_dump(exclude={"password"})
    update_dict["hashed_password"] = hash_password(user_data.password)

    updated = await UserRepository.update(db, user, update_dict)
    return UserSchema.model_validate(updated)


async def delete_user(user_id: UUID, db: AsyncSession) -> UserSchema:
    user = await UserRepository.delete(db, user_id)
    if not user:
        raise AccountNotFound("User not found")
    return UserSchema.model_validate(user)
