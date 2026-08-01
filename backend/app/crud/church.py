from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.church import Church
from app.models.council import Council
from app.schemas.church import ChurchCreate, ChurchUpdate


def create_church(db: Session, church: ChurchCreate):

    if church.council_id:

        council = db.query(Council).filter(
            Council.id == church.council_id
        ).first()

        if not council:
            raise HTTPException(
                status_code=404,
                detail="Council not found"
            )

    db_church = Church(**church.model_dump())

    db.add(db_church)
    db.commit()
    db.refresh(db_church)

    return db_church

def get_churches(db: Session):
    return db.query(Church).all()


def get_church(db: Session, church_id: int):

    church = db.query(Church).filter(
        Church.id == church_id
    ).first()

    if not church:
        raise HTTPException(
            status_code=404,
            detail="Church not found"
        )

    return church


def update_church(
    db: Session,
    church_id: int,
    church_data: ChurchUpdate,
):

    church = db.query(Church).filter(
        Church.id == church_id
    ).first()

    if not church:
        raise HTTPException(
            status_code=404,
            detail="Church not found"
        )

    if church_data.council_id:

        council = db.query(Council).filter(
            Council.id == church_data.council_id
        ).first()

        if not council:
            raise HTTPException(
                status_code=404,
                detail="Council not found"
            )

    update_data = church_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(church, key, value)

    db.commit()
    db.refresh(church)

    return church


def delete_church(
    db: Session,
    church_id: int,
):

    church = db.query(Church).filter(
        Church.id == church_id
    ).first()

    if not church:
        raise HTTPException(
            status_code=404,
            detail="Church not found"
        )

    church.is_active = False

    db.commit()
    db.refresh(church)

    return church

