from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChurchBase(BaseModel):
    council_id: int | None = None
    name: str
    address: str | None = None
    city: str | None = None
    country: str | None = None
    phone: str | None = None
    email: str | None = None
    pastor_name: str | None = None
    is_active: bool = True


class ChurchCreate(ChurchBase):
    pass


class ChurchUpdate(BaseModel):
    council_id: int | None = None
    name: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    phone: str | None = None
    email: str | None = None
    pastor_name: str | None = None
    is_active: bool | None = None


class ChurchResponse(ChurchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)