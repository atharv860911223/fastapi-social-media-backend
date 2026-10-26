"""add foreign-key to post_f table

Revision ID: 26d4aec7a82f
Revises: 2fc595b3f46a
Create Date: 2026-10-26 14:05:54.280440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26d4aec7a82f'
down_revision: Union[str, Sequence[str], None] = '2fc595b3f46a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts_f', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts_f', referent_table="users_f",
    local_cols=['owner_id'], remote_cols=["id"], ondelete="CAsCADE")

def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts_f")
    op.drop_column('posts_f', 'owner_id')
