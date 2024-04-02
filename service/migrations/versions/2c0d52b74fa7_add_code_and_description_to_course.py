"""Add code and description to course

Revision ID: 2c0d52b74fa7
Revises: 78d57585eaec
Create Date: 2024-04-02 09:58:38.168984
"""
import sys
import pathlib

BASE_PATH = pathlib.Path(__file__).parent.resolve()
sys.path.append(BASE_PATH.parent.parent.resolve())

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import update

from settings import SUPPORTED_COURSES
from database.models import Course

revision: str = '2c0d52b74fa7'
down_revision: Union[str, None] = '78d57585eaec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    session = op.get_bind()

    op.add_column('course', sa.Column('code', sa.String(), nullable=True))
    op.add_column('course', sa.Column('description', sa.String(), nullable=True))

    for code, course in SUPPORTED_COURSES.items():
        session.execute(
            update(Course).where(
                Course.name == course["NAME"]
            ).values(
                code=code, description=course["DESCRIPTION"]
            )
        )

    op.alter_column('course', 'code', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('course', 'description', existing_type=sa.VARCHAR(), nullable=False)


def downgrade() -> None:
    op.drop_column('course', 'description')
    op.drop_column('course', 'code')
