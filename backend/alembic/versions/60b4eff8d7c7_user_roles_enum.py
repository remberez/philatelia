"""user roles enum

Revision ID: 60b4eff8d7c7
Revises: 97de23dbfa42
Create Date: 2025-05-06 03:50:16.460176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60b4eff8d7c7'
down_revision: Union[str, None] = '97de23dbfa42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создаём тип Enum вручную
    op.execute("CREATE TYPE userroles AS ENUM ('ADMIN', 'USER')")

    # Заполняем все NULL значения в столбце role значением по умолчанию 'USER'
    op.execute("UPDATE \"user\" SET role = 'USER' WHERE role IS NULL")

    # Преобразуем столбец "role" в новый тип Enum и устанавливаем его как NOT NULL
    op.alter_column('user', 'role',
                    existing_type=sa.VARCHAR(),
                    type_=sa.Enum('ADMIN', 'USER', name='userroles'),
                    nullable=False,
                    postgresql_using="role::userroles")

def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем тип Enum, если он больше не используется
    op.execute("DROP TYPE IF EXISTS userroles")

    # Изменяем столбец обратно
    op.alter_column('user', 'role',
                    existing_type=sa.Enum('ADMIN', 'USER', name='userroles'),
                    type_=sa.VARCHAR(),
                    nullable=True)
