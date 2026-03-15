-- 001_initial_migration.sql
-- Initial schema migration

CREATE TABLE IF NOT EXISTS users (
    id          UUID PRIMARY KEY,
    email       VARCHAR NOT NULL UNIQUE,
    username    VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_users_email    ON users (email);
CREATE INDEX IF NOT EXISTS ix_users_username ON users (username);

CREATE TABLE IF NOT EXISTS admins (
    id          UUID PRIMARY KEY,
    email       VARCHAR NOT NULL UNIQUE,
    username    VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_admins_email    ON admins (email);
CREATE INDEX IF NOT EXISTS ix_admins_username ON admins (username);

CREATE TABLE IF NOT EXISTS flowers (
    id       UUID PRIMARY KEY,
    name     VARCHAR NOT NULL,
    price    DOUBLE PRECISION NOT NULL,
    quantity INTEGER NOT NULL
);
