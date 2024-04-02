import pytest
from sqlalchemy import select

from database.models import Course, UserCourse


class TestUserCourse:
    @pytest.mark.asyncio
    async def test_activate(self, async_session, user):
        async with async_session() as session:
            courses = await session.scalars(select(Course))

            for course in courses.all():
                await UserCourse.activate(course.id, user.id)

                assert await session.scalar(
                    select(
                        UserCourse
                    ).where(
                        UserCourse.is_active,
                        UserCourse.user_id == user.id,
                        UserCourse.course_id == course.id
                    )
                )

    @pytest.mark.asyncio
    async def test_multiple_activations(self, async_session, user):
        async with async_session() as session:
            courses = await session.scalars(select(Course))

            for course in courses.all():
                await UserCourse.activate(course.id, user.id)
                await UserCourse.activate(course.id, user.id)

                assert await session.scalar(
                    select(
                        UserCourse
                    ).where(
                        UserCourse.is_active,
                        UserCourse.user_id == user.id,
                        UserCourse.course_id == course.id
                    )
                )
