-- 002_add_address_to_users.sql
-- Add address column to users table

ALTER TABLE users ADD COLUMN IF NOT EXISTS address VARCHAR NOT NULL;
