"""Rename course

Revision ID: e6b629f1fbcb
Revises: 2c0d52b74fa7
Create Date: 2024-04-02 10:38:55.343407
"""
import sys
import pathlib

BASE_PATH = pathlib.Path(__file__).parent.resolve()
sys.path.append(BASE_PATH.parent.parent.resolve())

from typing import Sequence, Union

from alembic import op
from sqlalchemy import update

from settings import SUPPORTED_COURSES
from database.models import Course

revision: str = 'e6b629f1fbcb'
down_revision: Union[str, None] = '2c0d52b74fa7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    session = op.get_bind()

    for code, course in SUPPORTED_COURSES.items():
        session.execute(
            update(Course).where(
                Course.code == code
            ).values(name=course["NAME"])
        )


def downgrade() -> None:
    pass
