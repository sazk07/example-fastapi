"""add_posts_content_column_to_posts_table

Revision ID: c7cf7f9cef9f
Revises: 8080d1d64e5f
Create Date: 2022-08-23 23:06:05.011484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7cf7f9cef9f'
down_revision = '8080d1d64e5f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("posts_content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "posts_content")
    pass