from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from .base import Model


class UserCourse(Model):
    user_id = Column(Integer, ForeignKey("user.id"))
    course_id = Column(Integer, ForeignKey("course.id"))


class Course(Model):
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    users = relationship("User", secondary="user_course", back_populates="courses")
    questions = relationship(
        "Question", backref=backref("course", cascade="all,delete"), lazy=True
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.name} ({self.code})"
