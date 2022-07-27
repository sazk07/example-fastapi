"""add users table

Revision ID: 4945fe8243cc
Revises: 3b8b790de0e6
Create Date: 2022-07-26 22:01:23.023212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4945fe8243cc"
down_revision = "3b8b790de0e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("users_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("users_id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
