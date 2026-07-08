"""create users table

Revision ID: a09769e5e09c
Revises:
Create Date: 2026-05-07 09:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "a09769e5e09c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "role",
            sa.Enum("student", "professor", "admin", name="userrole", native_enum=False),
            nullable=False,
        ),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("ra", sa.String(length=50), nullable=True),
        sa.Column("profile_picture", sa.LargeBinary(), nullable=True),
        sa.CheckConstraint(
            "role = 'student' OR ra IS NULL",
            name="ck_users_ra_only_for_students",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_ra"), "users", ["ra"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_ra"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
