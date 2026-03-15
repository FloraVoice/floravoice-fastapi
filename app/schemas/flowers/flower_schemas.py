from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class FlowerCreate(BaseModel):
    name: str
    price: float
    quantity: int


class FlowerUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None


class FlowerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    price: float
    quantity: int

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)
