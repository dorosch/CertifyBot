"""Add is_active to UserCourse

Revision ID: a212e4c61c5a
Revises: 80385fbfb644
Create Date: 2024-04-02 13:51:38.886572
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a212e4c61c5a'
down_revision: Union[str, None] = '80385fbfb644'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_course', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.create_unique_constraint('user_course_unique', 'user_course', ['user_id', 'course_id'])


def downgrade() -> None:
    op.drop_constraint('user_course_unique', 'user_course', type_='unique')
    op.drop_column('user_course', 'is_active')
