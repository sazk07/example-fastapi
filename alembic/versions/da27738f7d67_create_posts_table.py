"""create posts table

Revision ID: da27738f7d67
Revises: 
Create Date: 2022-07-26 21:37:06.815149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "da27738f7d67"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("posts_id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
