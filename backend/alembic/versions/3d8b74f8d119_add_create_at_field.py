"""add create_at field

Revision ID: 3d8b74f8d119
Revises: 635392773fbb
Create Date: 2025-05-06 06:42:06.410260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d8b74f8d119'
down_revision: Union[str, None] = '635392773fbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('post', sa.Column('created_at', sa.TIMESTAMP(timezone=False), server_default=sa.func.now(), nullable=False))

def downgrade():
    op.drop_column('post', 'created_at')