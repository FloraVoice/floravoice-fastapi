from pydantic import BaseModel, EmailStr

from app.schemas.auth.common import Account


class UserBase(BaseModel):
    email: EmailStr
    username: str
    phone_number: str
    address: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(Account):
    phone_number: str
    address: str
