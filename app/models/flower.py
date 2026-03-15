from uuid import uuid4

from sqlalchemy import Column, String, Float, Integer, UUID

from app.db import Base


class Flower(Base):
    __tablename__ = "flowers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
