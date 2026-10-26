"""add content column to posts_f table

Revision ID: 4c105f975107
Revises: e5d4243de576
Create Date: 2026-10-26 12:25:55.393055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c105f975107'
down_revision: Union[str, Sequence[str], None] = 'e5d4243de576'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts_f", sa.Column('content', sa.String(), nullable=False))
    


def downgrade() -> None:
    op.drop_column('posts_f', 'content')
    pass
