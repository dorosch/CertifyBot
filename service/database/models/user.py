from sqlalchemy import Column, String, Integer

from .base import Model


class User(Model):
    tg_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
