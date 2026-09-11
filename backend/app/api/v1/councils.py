from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.db.session import get_db

from app.crud.council import (
    create_council,
    get_councils,
    get_council,
    update_council,
    deactivate_council,
)

from app.schemas.council import (
    CouncilCreate,
    CouncilUpdate,
    CouncilResponse,
)


router = APIRouter(
    prefix="/councils",
    tags=["Councils"],
)


@router.post(
    "/",
    response_model=CouncilResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_council(
    council: CouncilCreate,
    current_user: User = Depends(
        require_role("super_admin")
    ),
    db: Session = Depends(get_db),
):
    return create_council(
        db,
        council,
    )


@router.get(
    "/",
    response_model=List[CouncilResponse],
)
def read_councils(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return get_councils(db)


@router.get(
    "/{council_id}",
    response_model=CouncilResponse,
)
def read_council(
    council_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return get_council(
        db,
        council_id,
    )


@router.put(
    "/{council_id}",
    response_model=CouncilResponse,
)
def edit_council(
    council_id: int,
    council: CouncilUpdate,
    current_user: User = Depends(
        require_role("super_admin")
    ),
    db: Session = Depends(get_db),
):
    return update_council(
        db,
        council_id,
        council,
    )


@router.delete(
    "/{council_id}",
    response_model=CouncilResponse,
)
def remove_council(
    council_id: int,
    current_user: User = Depends(
        require_role("super_admin")
    ),
    db: Session = Depends(get_db),
):
    return deactivate_council(
        db,
        council_id,
    )