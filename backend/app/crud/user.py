from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.church import Church
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

def can_manage_user(
    current_user: User,
    target_role: str,
):
    if current_user.role == "super_admin":
        return

    if current_user.role == "admin":
        if target_role != "secretary":
            raise HTTPException(
                status_code=403,
                detail="Admins can only manage secretaries",
            )

        return

    raise HTTPException(
        status_code=403,
        detail="You do not have permission to manage users",
    )
    
def create_user(
    db: Session,
    user: UserCreate,
    current_user: User,
):
    # Solo super_admin puede crear usuarios sin iglesia
    # o asignarlos a cualquier iglesia.
    if current_user.role != "super_admin":

        if user.church_id != current_user.church_id:
            raise HTTPException(
                status_code=403,
                detail="You can only create users in your church",
            )
        # Un admin no puede crear super_admin.
        can_manage_user(
    current_user,
    user.role,
)
        if user.church_id is not None:
            church = db.query(Church).filter(
                Church.id == user.church_id
            ).first()
            
            
            if not church:
                raise HTTPException(
                      status_code=404,
                      detail="Church not found",
                )

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    db_user = User(
        church_id=user.church_id,
        full_name=user.full_name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role,
        is_active=user.is_active,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_email(
    db: Session,
    email: str,
):
    return db.query(User).filter(
        User.email == email
    ).first()


def get_users(
    db: Session,
    current_user: User,
):
    if current_user.role == "super_admin":
        return db.query(User).all()

    return (
        db.query(User)
        .filter(
            User.church_id == current_user.church_id
        )
        .all()
    )


def get_user(
    db: Session,
    user_id: int,
    current_user: User,
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if current_user.role != "super_admin":
        if user.church_id != current_user.church_id:
            raise HTTPException(
                status_code=403,
                detail="You can only access users in your church",
            )

    return user


def update_user(
    db: Session,
    user_id: int,
    user_update: UserUpdate,
    current_user: User,
):
    user = get_user(
        db,
        user_id,
        current_user,
    )
    if current_user.role == "admin":
        if user.role != "secretary":
            raise HTTPException(
                status_code=403,
                detail="Admins can only manage secretaries",
        )
    update_data = user_update.model_dump(
        exclude_unset=True
    )
    if "role" in update_data:
        can_manage_user(
        current_user,
        update_data["role"],
    )
    if "church_id" in update_data:

        new_church_id = update_data["church_id"]

        if current_user.role != "super_admin":
            if new_church_id != current_user.church_id:
                raise HTTPException(
                    status_code=403,
                    detail="You cannot move a user to another church",
                )

        church = db.query(Church).filter(
            Church.id == new_church_id
        ).first()

        if not church:
            raise HTTPException(
                status_code=404,
                detail="Church not found",
            )

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(
            update_data.pop("password")
        )

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user_id: int,
    current_user: User,
):
    user = get_user(
        db,
        user_id,
        current_user,
    )

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate yourself",
        )

    user.is_active = False

    db.commit()
    db.refresh(user)

    return user