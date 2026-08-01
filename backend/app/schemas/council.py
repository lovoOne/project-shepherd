from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CouncilBase(BaseModel):
    name: str
    country: str
    email: str | None = None
    phone: str | None = None
    president_name: str
    is_active: bool = True


class CouncilCreate(CouncilBase):
    pass


class CouncilUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
    email: str | None = None
    phone: str | None = None
    president_name: str | None = None
    is_active: bool | None = None


class CouncilResponse(CouncilBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)