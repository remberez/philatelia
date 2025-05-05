"""change pass hash type

Revision ID: 97de23dbfa42
Revises: e587c2380c27
Create Date: 2025-05-06 03:41:52.188348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97de23dbfa42'
down_revision: Union[str, None] = 'e587c2380c27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("user", "hashed_pass",
                    existing_type=sa.BigInteger(),
                    type_=sa.String(),
                    existing_nullable=True)

def downgrade() -> None:
    op.alter_column("user", "hashed_pass",
                    existing_type=sa.String(),
                    type_=sa.BigInteger(),
                    existing_nullable=True)
