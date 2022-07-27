"""add posts_content column to posts table

Revision ID: 3b8b790de0e6
Revises: da27738f7d67
Create Date: 2022-07-26 21:50:58.539531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3b8b790de0e6"
down_revision = "da27738f7d67"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("posts_content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "posts_content")
    pass
