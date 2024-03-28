"""Fill data SAA-C03

Revision ID: 97e45c2507c6
Revises: 8caeed8a5a33
Create Date: 2024-03-27 19:44:51.767786
"""
import sys
import pathlib

BASE_PATH = pathlib.Path(__file__).parent.resolve()
sys.path.append(BASE_PATH.parent.parent.resolve())

import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import select, insert, delete

from settings import SUPPORTED_COURCES
from database.models import Course, Question, Answer

revision: str = "97e45c2507c6"
down_revision: Union[str, None] = "8caeed8a5a33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

COURSE = SUPPORTED_COURCES["SAA-C03"]
COURSE_NAME = COURSE["name"]
COURSE_QUESTIONS = COURSE["questions"]


def load_data() -> list[dict]:
    with open(COURSE_QUESTIONS) as file:
        return json.load(file)


def upgrade() -> None:
    data = load_data()
    session = op.get_bind()

    session.execute(
        insert(Course).values({
            "name": COURSE_NAME
        })
    )
    course_id = session.execute(
        select(Course.id).where(Course.name == COURSE_NAME)
    ).scalar()

    for question in data:
        answers = question.pop("answers")

        session.execute(
            insert(Question).values({**question, "course_id": course_id})
        )
        question_id = session.execute(
            select(Question.id).where(Question.text == question["text"])
        ).scalar()

        session.execute(
            insert(Answer).values([{**answer, "question_id": question_id} for answer in answers])
        )


def downgrade() -> None:
    data = load_data()
    session = op.get_bind()

    for question in data:
        answers = [answer["text"] for answer in question.pop("answers")]

        session.execute(
            delete(Answer).where(Answer.text.in_(answers))
        )
        session.execute(
            delete(Question).where(Question.text == question["text"])
        )

    session.execute(
        delete(Course).where(Course.name == COURSE_NAME)
    )
