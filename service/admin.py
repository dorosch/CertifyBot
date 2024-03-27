from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

from database import engine
from database.models import User, Course, Question, Answer


class UserAdmin(ModelView, model=User):
    column_list = (
        User.id,
        User.tg_id,
        User.first_name,
        User.last_name,
        User.created_at
    )


class CourseAdmin(ModelView, model=Course):
    column_list = (
        Course.id,
        Course.name
    )


class QuestionAdmin(ModelView, model=Question):
    column_list = (
        Question.id,
        Question.course_id
    )


class AnswerAdmin(ModelView, model=Answer):
    column_list = (
        Answer.id,
        Answer.question_id,
        Answer.text,
        Answer.is_correct
    )


app = FastAPI()
admin = Admin(app, engine, base_url="/")

admin.add_view(UserAdmin)
admin.add_view(CourseAdmin)
admin.add_view(QuestionAdmin)
admin.add_view(AnswerAdmin)
