from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Church(Base):
    __tablename__ = "churches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    council_id: Mapped[int | None] = mapped_column(
        ForeignKey("councils.id"),
        nullable=True,
)

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    address: Mapped[str] = mapped_column(String(255), nullable=True)

    city: Mapped[str] = mapped_column(String(100), nullable=True)

    country: Mapped[str] = mapped_column(String(100), nullable=True)

    phone: Mapped[str] = mapped_column(String(30), nullable=True)

    email: Mapped[str] = mapped_column(String(150), nullable=True)

    pastor_name: Mapped[str] = mapped_column(String(150), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    council = relationship("Council", back_populates="churches")
    
    members = relationship("Member", back_populates="church",)