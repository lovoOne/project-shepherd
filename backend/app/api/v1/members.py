from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud.member import (
    create_member,
    delete_member,
    get_member,
    get_members,
    update_member,
)
from app.db.session import get_db
from app.schemas.member import (
    MemberCreate,
    MemberResponse,
    MemberUpdate,
)

router = APIRouter(
    prefix="/members",
    tags=["Members"],
)


@router.get(
    "/",
    response_model=List[MemberResponse],
)
def read_members(
    db: Session = Depends(get_db),
):
    return get_members(db)


@router.post(
    "/",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_member(
    member: MemberCreate,
    db: Session = Depends(get_db),
):
    return create_member(db, member)


@router.get(
    "/{member_id}",
    response_model=MemberResponse,
)
def read_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    return get_member(db, member_id)


@router.put(
    "/{member_id}",
    response_model=MemberResponse,
)
def edit_member(
    member_id: int,
    member: MemberUpdate,
    db: Session = Depends(get_db),
):
    return update_member(
        db,
        member_id,
        member,
    )


@router.delete(
    "/{member_id}",
    response_model=MemberResponse,
)
def remove_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    return delete_member(
        db,
        member_id,
    )