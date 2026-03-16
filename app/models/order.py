from uuid import uuid4
from datetime import datetime, UTC
from sqlalchemy import Column, UUID, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from app.db import Base


class Order(Base):
    __tablename__ = "orders"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    items      = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="selectin")


class OrderItem(Base):
    __tablename__ = "order_items"
    id                = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id          = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    flower_id         = Column(UUID(as_uuid=True), ForeignKey("flowers.id"), nullable=False)
    quantity          = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)
    order             = relationship("Order", back_populates="items")
