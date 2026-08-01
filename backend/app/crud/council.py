from sqlalchemy.orm import Session

from app.models.council import Council
from app.schemas.council import CouncilCreate


def create_council(db: Session, council: CouncilCreate) -> Council:
    db_council = Council(**council.model_dump())

    db.add(db_council)
    db.commit()
    db.refresh(db_council)

    return db_council

def get_councils(db: Session):
    return db.query(Council).all()

def get_council(db: Session, council_id: int):
    return (
        db.query(Council)
        .filter(Council.id == council_id)
        .first()
    )
    
    
from app.schemas.council import CouncilUpdate


def update_council(
    db: Session,
    council_id: int,
    council_data: CouncilUpdate,
):
    council = (
        db.query(Council)
        .filter(Council.id == council_id)
        .first()
    )

    if not council:
        return None

    update_data = council_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(council, key, value)

    db.commit()
    db.refresh(council)

    return council

def deactivate_council(db: Session, council_id: int):
    council = (
        db.query(Council)
        .filter(Council.id == council_id)
        .first()
    )

    if not council:
        return None

    council.is_active = False

    db.commit()
    db.refresh(council)

    return council

def deactivate_council(db: Session, council_id: int):
    council = (
        db.query(Council)
        .filter(Council.id == council_id)
        .first()
    )

    if council is None:
        return None

    council.is_active = False

    db.commit()
    db.refresh(council)

    return council


from fastapi import HTTPException


def delete_council(db: Session, council_id: int):
    council = db.query(Council).filter(Council.id == council_id).first()

    if not council:
        raise HTTPException(
            status_code=404,
            detail="Council not found"
        )

    db.delete(council)
    db.commit()

    return {"message": "Council deleted successfully"}