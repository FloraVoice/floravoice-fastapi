-- 004_add_phone_number_to_users.sql
-- Convert users to customer records for voice-agent lookup

ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_phone_number ON users (phone_number);
ALTER TABLE users DROP COLUMN IF EXISTS hashed_password;
