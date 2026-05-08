from __future__ import annotations

from datetime import date
from enum import StrEnum

from sqlalchemy import Boolean, CheckConstraint, Enum, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from database.config.base import Base


class UserRole(StrEnum):
    STUDENT = "student"
    PROFESSOR = "professor"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role = 'student' OR ra IS NULL", name="ck_users_ra_only_for_students"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            native_enum=False,
            values_callable=lambda enum_class: [member.value for member in enum_class],
        ),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    ra: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True, index=True)
    profile_picture: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
