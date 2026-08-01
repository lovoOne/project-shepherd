from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.church import Church
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate


def create_member(db: Session, member: MemberCreate):

    church = db.query(Church).filter(
        Church.id == member.church_id
    ).first()

    if not church:
        raise HTTPException(
            status_code=404,
            detail="Church not found"
        )

    db_member = Member(**member.model_dump())

    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member


def get_members(db: Session):
    return db.query(Member).all()


def get_member(db: Session, member_id: int):

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member


def update_member(
    db: Session,
    member_id: int,
    member_update: MemberUpdate,
):

    member = get_member(db, member_id)

    if member_update.church_id is not None:

        church = db.query(Church).filter(
            Church.id == member_update.church_id
        ).first()

        if not church:
            raise HTTPException(
                status_code=404,
                detail="Church not found"
            )

    update_data = member_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)

    return member


def delete_member(
    db: Session,
    member_id: int,
):

    member = get_member(db, member_id)

    member.is_active = False

    db.commit()
    db.refresh(member)

    return member