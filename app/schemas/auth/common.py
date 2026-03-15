from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer


class AccountBase(BaseModel):
    email: EmailStr
    username: str


class AccountCreate(AccountBase):
    email: EmailStr
    username: str
    password: str


class AccountUpdatePassword(BaseModel):
    password: str


class Account(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)


class AccountLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str