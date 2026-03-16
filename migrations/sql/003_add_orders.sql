-- 003_add_orders.sql
-- Add orders and order_items tables

CREATE TABLE IF NOT EXISTS orders (
    id         UUID PRIMARY KEY,
    user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_orders_user_id ON orders (user_id);

CREATE TABLE IF NOT EXISTS order_items (
    id                UUID PRIMARY KEY,
    order_id          UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    flower_id         UUID NOT NULL REFERENCES flowers(id),
    quantity          INTEGER NOT NULL,
    price_at_purchase DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_order_items_order_id  ON order_items (order_id);
CREATE INDEX IF NOT EXISTS ix_order_items_flower_id ON order_items (flower_id);
