"""add user table

Revision ID: 2fc595b3f46a
Revises: 4c105f975107
Create Date: 2026-10-26 13:57:47.171019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fc595b3f46a'
down_revision: Union[str, Sequence[str], None] = '4c105f975107'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users_f',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa. String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                server_default=sa.text('now()'), nullable=False),
        sa. PrimaryKeyConstraint('id'),
        sa. UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users_f')
