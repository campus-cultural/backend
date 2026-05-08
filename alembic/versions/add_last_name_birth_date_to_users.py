"""add last_name and birth_date to users

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-05-07

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: str | None = "a09769e5e09c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("last_name", sa.String(255), nullable=True))
    op.add_column("users", sa.Column("birth_date", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "birth_date")
    op.drop_column("users", "last_name")
