"""Fill data SAA-C03

Revision ID: 97e45c2507c6
Revises: 8caeed8a5a33
Create Date: 2024-03-27 19:44:51.767786
"""
import sys
import pathlib

BASE_PATH = pathlib.Path(__file__).parent.resolve()
sys.path.append(BASE_PATH.parent.parent.resolve())

from typing import Sequence, Union

from alembic import op

from migrations.helpers import CourseHelper

revision: str = "97e45c2507c6"
down_revision: Union[str, None] = "8caeed8a5a33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    CourseHelper.create("SAA-C03")


def downgrade() -> None:
    CourseHelper.remove("SAA-C03")
