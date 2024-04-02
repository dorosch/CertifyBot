import pytest
from sqlalchemy import select

from main import StartCommandHandler
from settings import SUPPORTED_COURSES
from database.models import User, Course


class TestStartHandler:
    @pytest.mark.asyncio
    async def test_handler_send_answer(self, message):
        await StartCommandHandler(message).handle()

        assert message.answers is not None

    @pytest.mark.asyncio
    async def test_user_is_create(self, message, async_session):
        await StartCommandHandler(message).handle()

        async with async_session() as session:
            result = await session.scalars(
                select(User).where(User.tg_id == message.from_user.id)
            )

            assert result.one_or_none()

    @pytest.mark.asyncio
    async def test_courses_answer(self, message, async_session):
        await StartCommandHandler(message).handle()

        async with async_session() as session:
            result = await session.scalars(select(Course))

            assert len(result.all()) == len(message.answers)
            assert len(SUPPORTED_COURSES) == len(message.answers)
