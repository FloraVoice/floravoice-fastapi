from app.schemas.auth.common import AccountCreate, AccountLogin, Account


class AdminCreate(AccountCreate):
    pass


class AdminUpdate(AccountCreate):
    pass


class AdminLogin(AccountLogin):
    pass


class Admin(Account):
    pass
