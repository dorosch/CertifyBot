import json

from alembic import op
from sqlalchemy.sql import select, insert, delete

from settings import SUPPORTED_COURSES
from database.models import Course, Question, Answer


class CourseHelper:
    """This helper is used in migrations to reduce code duplication."""

    @staticmethod
    def create(course: str):
        session = op.get_bind()

        course_code = course
        course_name = SUPPORTED_COURSES[course]["NAME"]
        course_link = SUPPORTED_COURSES[course]["LINK"]
        course_description = SUPPORTED_COURSES[course]["DESCRIPTION"]
        course_questions = SUPPORTED_COURSES[course]["QUESTIONS"]

        session.execute(
            insert(Course).values({
                "code": course_code,
                "name": course_name,
                "link": course_link,
                "description": course_description
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
            session.commit()

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
            session.commit()

        session.execute(
            delete(Course).where(Course.name == course_name)
        )
        session.commit()
