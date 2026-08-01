from typing import List


from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
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
from app.db.session import get_db
from app.schemas.council import CouncilCreate, CouncilResponse

router = APIRouter(prefix="/councils", tags=["Councils"])


@router.post(
    "/",
    response_model=CouncilResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_council(
    council: CouncilCreate,
    db: Session = Depends(get_db),
):
    return create_council(db, council)

@router.get(
    "/",
    response_model=List[CouncilResponse],
)
def read_councils(
    db: Session = Depends(get_db),
):
    return get_councils(db)

from fastapi import HTTPException

@router.get(
    "/{council_id}",
    response_model=CouncilResponse,
)
def read_council(
    council_id: int,
    db: Session = Depends(get_db),
):
    council = get_council(db, council_id)

    if council is None:
        raise HTTPException(
            status_code=404,
            detail="Council not found",
        )

    return council

@router.put(
    "/{council_id}",
    response_model=CouncilResponse,
)
def edit_council(
    council_id: int,
    council: CouncilUpdate,
    db: Session = Depends(get_db),
):
    updated = update_council(
        db,
        council_id,
        council,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Council not found",
        )

    return updated

@router.delete(
    "/{council_id}",
    response_model=CouncilResponse,
)
def delete_council(
    council_id: int,
    db: Session = Depends(get_db),
):
    council = deactivate_council(db, council_id)

    if council is None:
        raise HTTPException(
            status_code=404,
            detail="Council not found",
        )

    return council

@router.delete(
    "/{council_id}",
    response_model=CouncilResponse,
)
def delete_council(
    council_id: int,
    db: Session = Depends(get_db),
):
    council = deactivate_council(db, council_id)

    if council is None:
        raise HTTPException(
            status_code=404,
            detail="Council not found",
        )

    return council

from app.crud.council import delete_council

@router.delete(
    "/{council_id}",
)
def remove_council(
    council_id: int,
    db: Session = Depends(get_db),
):
    return delete_council(db, council_id)