from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    church_id: Mapped[int] = mapped_column(
        ForeignKey("churches.id"),
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    gender: Mapped[str] = mapped_column(String(20), nullable=False)

    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)

    baptized: Mapped[bool] = mapped_column(Boolean, default=False)
    baptism_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    join_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    church = relationship("Church", back_populates="members")