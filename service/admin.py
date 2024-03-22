from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

from database import engine
from database.models import User


class UserAdmin(ModelView, model=User):
    column_list = (
        User.id,
        User.tg_id,
        User.first_name,
        User.last_name,
        User.created_at
    )


app = FastAPI()
admin = Admin(app, engine, base_url="/")

admin.add_view(UserAdmin)
