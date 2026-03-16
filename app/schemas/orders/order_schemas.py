from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field, field_serializer


class OrderItemCreate(BaseModel):
    flower_id: UUID
    quantity:  int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:                UUID
    flower_id:         UUID
    quantity:          int
    price_at_purchase: float

    @field_serializer("id", "flower_id")
    def serialize_uuid(self, v: UUID, _info):
        return str(v)


class OrderCreate(BaseModel):
    user_id: UUID
    items:   List[OrderItemCreate] = Field(..., min_length=1)


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:         UUID
    user_id:    UUID
    created_at: datetime
    items:      List[OrderItemResponse]

    @field_serializer("id", "user_id")
    def serialize_uuid(self, v: UUID, _info):
        return str(v)
