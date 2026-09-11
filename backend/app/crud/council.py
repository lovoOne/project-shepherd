from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.council import Council
from app.schemas.council import (
    CouncilCreate,
    CouncilUpdate,
)


def create_council(
    db: Session,
    council: CouncilCreate,
):
    db_council = Council(
        **council.model_dump()
    )

    db.add(db_council)
    db.commit()
    db.refresh(db_council)

    return db_council


def get_councils(
    db: Session,
):
    return (
        db.query(Council)
        .all()
    )


def get_council(
    db: Session,
    council_id: int,
):
    council = (
        db.query(Council)
        .filter(
            Council.id == council_id
        )
        .first()
    )

    if not council:
        raise HTTPException(
            status_code=404,
            detail="Council not found",
        )

    return council


def update_council(
    db: Session,
    council_id: int,
    council_data: CouncilUpdate,
):
    council = get_council(
        db,
        council_id,
    )

    update_data = council_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            council,
            key,
            value,
        )

    db.commit()
    db.refresh(council)

    return council


def deactivate_council(
    db: Session,
    council_id: int,
):
    council = get_council(
        db,
        council_id,
    )

    council.is_active = False

    db.commit()
    db.refresh(council)

    return council