from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator


class MemberBase(BaseModel):
    church_id: int

    first_name: str
    last_name: str

    gender: Literal["masculino", "femenino"]

    birth_date: date | None = None

    phone: str | None = None
    email: str | None = None
    address: str | None = None

    baptized: bool = False
    baptism_date: date | None = None

    join_date: date | None = None

    is_active: bool = True


class MemberCreate(MemberBase):

    @model_validator(mode="after")
    def validate_baptism(self):
        if self.baptized and self.baptism_date is None:
            raise ValueError(
                "baptism_date is required when baptized is true"
            )

        if not self.baptized and self.baptism_date is not None:
            raise ValueError(
                "baptism_date must be null when baptized is false"
            )

        return self

class MemberUpdate(BaseModel):
    church_id: int | None = None

    first_name: str | None = None
    last_name: str | None = None
    gender: Literal["masculino","femenino"] | None = None

    birth_date: date | None = None

    phone: str | None = None
    email: str | None = None
    address: str | None = None

    baptized: bool | None = None
    baptism_date: date | None = None

    join_date: date | None = None

    is_active: bool | None = None
    
    
   # @model_validator(mode="after")
   # def validate_baptism(self):
    #  if self.baptized is True and self.baptism_date is None:
     #       raise ValueError(
      #          "baptism_date is required when baptized is true"
       #     )

        #if self.baptized is False and self.baptism_date is not None:
         #   raise ValueError(
          #      "baptism_date must be null when baptized is false"
           # )

     #   return self

class MemberResponse(MemberBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)