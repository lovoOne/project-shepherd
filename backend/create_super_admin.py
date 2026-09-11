from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User


db = SessionLocal()

try:
    email = "superadmin@projectshepherd.com"

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        print("El usuario ya existe.")
    else:
        super_admin = User(
            church_id=None,
            full_name="Project Shepherd Super Admin",
            email=email,
            hashed_password=get_password_hash("123456"),
            role="super_admin",
            is_active=True,
        )

        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)

        print("Super Admin creado correctamente.")
        print(f"ID: {super_admin.id}")
        print(f"Email: {super_admin.email}")
        print(f"Role: {super_admin.role}")

finally:
    db.close()