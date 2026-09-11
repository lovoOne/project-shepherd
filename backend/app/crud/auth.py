from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    create_access_token,
)
from app.models.user import User


def login_user(
    db: Session,
    email: str,
    password: str,
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    # Un usuario desactivado no puede iniciar sesión
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }