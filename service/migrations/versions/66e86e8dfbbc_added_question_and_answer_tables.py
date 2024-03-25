"""Added Question and Answer tables

Revision ID: 66e86e8dfbbc
Revises: 18647bd4e8cf
Create Date: 2024-03-25 11:25:14.134512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '66e86e8dfbbc'
down_revision: Union[str, None] = '18647bd4e8cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('question',
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
        sa.Column('question_id', sa.Integer(), nullable=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('answer')
    op.drop_table('question')
