from app.schemas.auth.common import AccountCreate, AccountLogin, Account


class UserCreate(AccountCreate):
    address: str


class UserUpdate(AccountCreate):
    address: str


class UserLogin(AccountLogin):
    pass


class User(Account):
    address: str
