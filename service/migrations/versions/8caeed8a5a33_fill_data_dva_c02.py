"""Fill data into Question and Answer tables

Revision ID: 8caeed8a5a33
Revises: 66e86e8dfbbc
Create Date: 2024-03-26 13:40:16.365071
"""
import sys
import pathlib

BASE_PATH = pathlib.Path(__file__).parent.resolve()
sys.path.append(BASE_PATH.parent.parent.resolve())

from typing import Sequence, Union

from alembic import op

from migrations.helpers import CourseHelper

revision: str = "8caeed8a5a33"
down_revision: Union[str, None] = "66e86e8dfbbc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    CourseHelper.create("DVA-C02")


def downgrade() -> None:
    CourseHelper.remove("DVA-C02")
