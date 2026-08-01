from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class MemberBase(BaseModel):
    church_id: int

    first_name: str
    last_name: str

    gender: str

    birth_date: date | None = None

    phone: str | None = None
    email: str | None = None
    address: str | None = None

    baptized: bool = False
    baptism_date: date | None = None

    join_date: date | None = None

    is_active: bool = True


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    church_id: int | None = None

    first_name: str | None = None
    last_name: str | None = None
    gender: str | None = None

    birth_date: date | None = None

    phone: str | None = None
    email: str | None = None
    address: str | None = None

    baptized: bool | None = None
    baptism_date: date | None = None

    join_date: date | None = None

    is_active: bool | None = None


class MemberResponse(MemberBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)