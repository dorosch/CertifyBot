"""Add AnswerHistory model

Revision ID: 80385fbfb644
Revises: e6b629f1fbcb
Create Date: 2024-04-02 12:54:13.001724
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '80385fbfb644'
down_revision: Union[str, None] = 'e6b629f1fbcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('answer_history',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('answer_history')
