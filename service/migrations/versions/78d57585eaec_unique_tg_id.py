"""unique tg_id

Revision ID: 78d57585eaec
Revises: 97e45c2507c6
Create Date: 2024-03-28 21:03:53.238576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '78d57585eaec'
down_revision: Union[str, None] = '97e45c2507c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'user', ['tg_id'])


def downgrade() -> None:
    op.drop_constraint(None, 'user', type_='unique')
