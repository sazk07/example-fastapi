"""add foreign key to posts table

Revision ID: 3e09fb0cb903
Revises: 4945fe8243cc
Create Date: 2022-07-27 10:25:29.714226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3e09fb0cb903"
down_revision = "4945fe8243cc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        "posts",
        "users",
        ["owner_id"],
        ["users_id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass
