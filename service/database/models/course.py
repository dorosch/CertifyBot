from sqlalchemy import (
    update, Column, String, Integer, ForeignKey, Boolean, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship, backref

from database import async_session

from .base import Model


class UserCourse(Model):
    user_id = Column(Integer, ForeignKey("user.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    is_active = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="user_course_unique"),
    )

    @staticmethod
    async def activate(course_id: int, user_id: int):
        """
        Make the course active for the user and deactivate all other courses.
        """

        async with async_session() as session:
            async with session.begin():
                # Deactivate all previous courses
                await session.execute(
                    update(
                        UserCourse
                    ).where(
                        user_id == user_id,
                        course_id == course_id
                    ).values(
                        is_active=False
                    )
                )

                # Activate current course
                await session.execute(
                    insert(
                        UserCourse
                    ).values(
                        user_id=user_id,
                        course_id=course_id,
                        is_active=True
                    ).on_conflict_do_update(
                        constraint="user_course_unique",
                        set_=dict(is_active=True)
                    )
                )
                await session.commit()


class Course(Model):
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    link = Column(String, nullable=False)
    users = relationship(
        "User", secondary="user_course", back_populates="courses"
    )
    questions = relationship(
        "Question", backref=backref("course", cascade="all,delete"), lazy=True
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.name} ({self.code})"
