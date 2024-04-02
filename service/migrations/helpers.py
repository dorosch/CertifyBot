import json

from alembic import op
from sqlalchemy.sql import select, insert, delete

from settings import SUPPORTED_COURSES
from database.models import Course, Question, Answer


class CourseHelper:
    """This helper is used in migrations to reduce code duplication."""
    # TODO: Fix reverse migrations with answer_question_id_fk constraint
    #       reproduction: alembic downgrade -3

    @staticmethod
    def create(course: str):
        session = op.get_bind()

        course_name = SUPPORTED_COURSES[course]["NAME"]
        course_questions = SUPPORTED_COURSES[course]["QUESTIONS"]

        session.execute(
            insert(Course).values({
                "name": course_name
            })
        )
        course_id = session.execute(
            select(Course.id).where(Course.name == course_name)
        ).scalar()

        for question in json.loads(course_questions.read_text()):
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

    @staticmethod
    def remove(course: str):
        session = op.get_bind()

        course_name = SUPPORTED_COURSES[course]["NAME"]
        course_questions = SUPPORTED_COURSES[course]["QUESTIONS"]

        for question in json.loads(course_questions.read_text()):
            answers = [answer["text"] for answer in question.pop("answers")]

            session.execute(
                delete(Answer).where(Answer.text.in_(answers))
            )
            session.execute(
                delete(Question).where(Question.text == question["text"])
            )

        session.execute(
            delete(Course).where(Course.name == course_name)
        )
