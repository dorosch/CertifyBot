from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Model


class UserCourse(Model):
    user_id = Column(Integer, ForeignKey("user.id"))
    course_id = Column(Integer, ForeignKey("course.id"))


class Course(Model):
    name = Column(String, nullable=False)
    users = relationship("User", secondary="user_course", back_populates="courses")
