from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.church import Church
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate
from app.models.user import User

def create_member(
    db: Session,
    member: MemberCreate,
    current_user: User,
):
    if current_user.role != "super_admin":
        if member.church_id != current_user.church_id:
            raise HTTPException(
                status_code=403,
                detail="You can only create members in your church",
            )

    church = db.query(Church).filter(
        Church.id == member.church_id
    ).first()

    if not church:
        raise HTTPException(
            status_code=404,
            detail="Church not found",
        )

    db_member = Member(
        **member.model_dump()
    )

    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member

#def get_members(db: Session):
#    return db.query(Member).all()
def get_members(
    db: Session,
    current_user: User,
    search: str | None = None,
    is_active: bool | None = None,
):
    if current_user.role == "super_admin":
        query = db.query(Member)
    else:
        query = db.query(Member).filter(
            Member.church_id == current_user.church_id
        )

    # Filtro por nombre o apellido
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                Member.first_name.ilike(search_term),
                Member.last_name.ilike(search_term),
            )
        )

    # Filtro por estado
    if is_active is not None:
        query = query.filter(
            Member.is_active == is_active
        )

    return query.all()

def get_member(
    db: Session,
    member_id: int,
    current_user: User,
):
    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    if current_user.role != "super_admin":
        if member.church_id != current_user.church_id:
            raise HTTPException(
                status_code=403,
                detail="You can only access members in your church",
            )

    return member


def update_member(
    db: Session,
    member_id: int,
    member_update: MemberUpdate,
    current_user: User,
):
    member = get_member(
        db,
        member_id,
        current_user,
    )

    # Verificar permisos de iglesia
    if current_user.role != "super_admin":

        if member.church_id != current_user.church_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update members in your church",
            )

        if (
            member_update.church_id is not None
            and member_update.church_id != current_user.church_id
        ):
            raise HTTPException(
                status_code=403,
                detail="You cannot move a member to another church",
            )

    # Verificar que la nueva iglesia exista
    if member_update.church_id is not None:

        church = db.query(Church).filter(
            Church.id == member_update.church_id
        ).first()

        if not church:
            raise HTTPException(
                status_code=404,
                detail="Church not found",
            )

    # Obtener solamente los campos enviados
    update_data = member_update.model_dump(
        exclude_unset=True
    )

    # --------------------------------------------------
    # VALIDACIÓN DEL ESTADO FINAL DEL BAUTISMO
    # --------------------------------------------------

    final_baptized = update_data.get(
        "baptized",
        member.baptized,
    )

    final_baptism_date = update_data.get(
        "baptism_date",
        member.baptism_date,
    )

    if final_baptized and final_baptism_date is None:
        raise HTTPException(
            status_code=422,
            detail="baptism_date is required when baptized is true",
        )

    if not final_baptized and final_baptism_date is not None:
        raise HTTPException(
            status_code=422,
            detail="baptism_date must be null when baptized is false",
        )

    # --------------------------------------------------
    # APLICAR CAMBIOS
    # --------------------------------------------------

    for key, value in update_data.items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)

    return member


def delete_member(
    db: Session,
    member_id: int,
    current_user: User,
):
    member = get_member(db, member_id, current_user)

    if current_user.role == "secretary":
        raise HTTPException(
            status_code=403,
            detail="Secretaries cannot deactivate members",
        )

    member.is_active = False

    db.commit()
    db.refresh(member)

    return member