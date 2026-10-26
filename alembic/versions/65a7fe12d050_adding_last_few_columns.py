"""adding last few columns

Revision ID: 65a7fe12d050
Revises: 26d4aec7a82f
Create Date: 2026-10-26 14:17:35.097480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65a7fe12d050'
down_revision: Union[str, Sequence[str], None] = '26d4aec7a82f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts_f', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")), )
    op.add_column('posts_f', sa.Column('rating', sa.Integer(), nullable=True), )
    pass


def downgrade() -> None:
    op.drop_column('posts_f', 'rating')
    op.drop_column('posts_f', 'created_at')

