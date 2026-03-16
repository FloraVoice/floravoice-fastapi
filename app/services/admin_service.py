from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from app.schemas.auth.admin_schemas import AdminCreate, AdminUpdate, Admin as AdminSchema
from app.repositories.admin_repository import AdminRepository
from app.dependancies.auth import hash_password
from app.exceptions.auth_exceptions import AccountAlreadyExist, AccountNotFound
from app.exceptions.common import DatabaseIntegrityError


async def create_admin(admin_data: AdminCreate, db: AsyncSession) -> AdminSchema:
    if await AdminRepository.select_by_email(db, admin_data.email):
        raise AccountAlreadyExist(f"Account with email '{admin_data.email}' already exists")

    if await AdminRepository.select_by_username(db, admin_data.username):
        raise AccountAlreadyExist(f"Account with username '{admin_data.username}' already exists")

    try:
        admin_dict = admin_data.model_dump(exclude={"password"})
        admin_dict["hashed_password"] = hash_password(admin_data.password)
        admin = await AdminRepository.insert(db, admin_dict)
        return AdminSchema.model_validate(admin)

    except IntegrityError as e:
        original = e.orig
        if isinstance(original, UniqueViolationError):
            raise AccountAlreadyExist("Account with this email or username already exists")
        else:
            raise DatabaseIntegrityError(str(original))


async def get_all_admins(db: AsyncSession) -> list[AdminSchema]:
    admins = await AdminRepository.select_all(db)
    return [AdminSchema.model_validate(a) for a in admins]


async def get_admin(admin_id: UUID, db: AsyncSession) -> AdminSchema:
    admin = await AdminRepository.select_by_id(db, admin_id)
    if not admin:
        raise AccountNotFound("Admin not found")
    return AdminSchema.model_validate(admin)


async def update_admin(admin_id: UUID, admin_data: AdminUpdate, db: AsyncSession) -> AdminSchema:
    admin = await AdminRepository.select_by_id(db, admin_id)
    if not admin:
        raise AccountNotFound("Admin not found")

    update_dict = admin_data.model_dump(exclude={"password"})
    update_dict["hashed_password"] = hash_password(admin_data.password)

    updated = await AdminRepository.update(db, admin, update_dict)
    return AdminSchema.model_validate(updated)


async def delete_admin(admin_id: UUID, db: AsyncSession) -> AdminSchema:
    admin = await AdminRepository.delete(db, admin_id)
    if not admin:
        raise AccountNotFound("Admin not found")
    return AdminSchema.model_validate(admin)
