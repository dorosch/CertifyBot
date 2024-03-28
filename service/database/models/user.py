from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base, relationship

from .base import Model


class User(Model):
    tg_id = Column(Integer, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    courses = relationship("Course", secondary="user_course", back_populates="users")

    def __str__(self) -> str:
        return f"{self.tg_id} - {self.username or 'anonymous'}"
