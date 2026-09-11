from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud.user import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
)
from app.db.session import get_db
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.core.dependencies import require_role
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    user: UserCreate,
    current_user: User = Depends(
        require_role("admin", "super_admin")
    ),
    db: Session = Depends(get_db),
):
    return create_user(
        db,
        user,
        current_user,
    )


@router.get(
    "/",
    response_model=List[UserResponse],
)
def read_users(
    current_user: User = Depends(
        require_role("admin", "super_admin")
    ),
    db: Session = Depends(get_db),
):
    return get_users(
        db,
        current_user,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def read_user(
    user_id: int,
    current_user: User = Depends(
        require_role("admin", "super_admin")
    ),
    db: Session = Depends(get_db),
):
    return get_user(
        db,
        user_id,
        current_user,
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def edit_user(
    user_id: int,
    user: UserUpdate,
    current_user: User = Depends(
        require_role("admin", "super_admin")
    ),
    db: Session = Depends(get_db),
):
    return update_user(
        db,
        user_id,
        user,
        current_user,
    )


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
)
def remove_user(
    user_id: int,
    current_user: User = Depends(
        require_role("admin", "super_admin")
    ),
    db: Session = Depends(get_db),
):
    return delete_user(
        db,
        user_id,
        current_user,
    )