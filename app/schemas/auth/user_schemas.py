from app.schemas.auth.common import AccountCreate, AccountLogin, Account


class UserCreate(AccountCreate):
    pass


class UserLogin(AccountLogin):
    pass 


class User(Account):
    pass
