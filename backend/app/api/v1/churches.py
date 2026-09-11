from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.models.user import User

from app.crud.church import (
    create_church,
    get_churches,
    get_church,
    update_church,
    delete_church,
)
from app.db.session import get_db
from app.schemas.church import (
    ChurchCreate,
    ChurchUpdate,
    ChurchResponse,
)


router = APIRouter(
    prefix="/churches",
    tags=["Churches"],
)


@router.post(
    "/",
    response_model=ChurchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_church(
    church: ChurchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_church(
        db,
        church,
        current_user,
    )


@router.get(
    "/",
    response_model=List[ChurchResponse],
)
def read_churches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_churches(
        db,
        current_user,
    )


@router.get(
    "/{church_id}",
    response_model=ChurchResponse,
)
def read_church(
    church_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_church(
        db,
        church_id,
        current_user,
    )


@router.put(
    "/{church_id}",
    response_model=ChurchResponse,
)
def edit_church(
    church_id: int,
    church: ChurchUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_church(
        db,
        church_id,
        church,
        current_user,
    )


@router.delete(
    "/{church_id}",
    response_model=ChurchResponse,
)
def remove_church(
    church_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_church(
        db,
        church_id,
        current_user,
    )