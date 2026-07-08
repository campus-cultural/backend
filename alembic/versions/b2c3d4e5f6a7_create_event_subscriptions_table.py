"""create event_subscriptions table

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-07-07 00:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "b2c3d4e5f6a7"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "event_subscriptions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "event_id", name="uq_event_subscriptions_user_event"),
    )
    op.create_index(
        op.f("ix_event_subscriptions_user_id"),
        "event_subscriptions",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_event_subscriptions_event_id"),
        "event_subscriptions",
        ["event_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_event_subscriptions_event_id"), table_name="event_subscriptions")
    op.drop_index(op.f("ix_event_subscriptions_user_id"), table_name="event_subscriptions")
    op.drop_table("event_subscriptions")
