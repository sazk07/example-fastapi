"""add_foreign_key_to_posts_table

Revision ID: 8080d1d64e5f
Revises: c2ca330523fb
Create Date: 2022-08-23 23:04:29.561065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8080d1d64e5f'
down_revision = 'c2ca330523fb'
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