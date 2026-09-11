from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.church import Church
from app.models.council import Council
from app.models.user import User
from app.schemas.church import ChurchCreate, ChurchUpdate


def create_church(
    db: Session,
    church: ChurchCreate,
    current_user: User,
):
    # Solo super_admin puede crear iglesias
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=403,
            detail="Only super_admin can create churches",
        )

    if church.council_id:
        council = db.query(Council).filter(
            Council.id == church.council_id
        ).first()

        if not council:
            raise HTTPException(
                status_code=404,
                detail="Council not found",
            )

    db_church = Church(**church.model_dump())

    db.add(db_church)
    db.commit()
    db.refresh(db_church)

    return db_church


def get_churches(
    db: Session,
    current_user: User,
):
    # super_admin puede ver todas
    if current_user.role == "super_admin":
        return db.query(Church).all()

    # Usuarios normales solamente su iglesia
    return (
        db.query(Church)
        .filter(Church.id == current_user.church_id)
        .all()
    )


def get_church(
    db: Session,
    church_id: int,
    current_user: User,
):
    church = db.query(Church).filter(
        Church.id == church_id
    ).first()

    if not church:
        raise HTTPException(
            status_code=404,
            detail="Church not found",
        )

    # super_admin puede acceder a cualquier iglesia
    if current_user.role == "super_admin":
        return church

    # Usuario normal solamente puede acceder a su iglesia
    if church.id != current_user.church_id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your church",
        )

    return church


def update_church(
    db: Session,
    church_id: int,
    church_data: ChurchUpdate,
    current_user: User,
):
    church = get_church(
        db,
        church_id,
        current_user,
    )

    # Solo super_admin puede cambiar el concilio
    if church_data.council_id is not None:

        if current_user.role != "super_admin":
            raise HTTPException(
                status_code=403,
                detail="Only super_admin can change the council",
            )

        council = db.query(Council).filter(
            Council.id == church_data.council_id
        ).first()

        if not council:
            raise HTTPException(
                status_code=404,
                detail="Council not found",
            )

    update_data = church_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(church, key, value)

    db.commit()
    db.refresh(church)

    return church


def delete_church(
    db: Session,
    church_id: int,
    current_user: User,
):
    church = get_church(
        db,
        church_id,
        current_user,
    )

    # Solo super_admin puede desactivar una iglesia
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=403,
            detail="Only super_admin can deactivate churches",
        )

    church.is_active = False

    db.commit()
    db.refresh(church)

    return church