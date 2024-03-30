import pytest
from sqlalchemy import select

from main import process_start_command
from database.models import User


class TestStartHandler:
    @pytest.mark.asyncio
    async def test_handler_send_answer(self, message):
        await process_start_command(message)

        assert message.text_answer is not None

    @pytest.mark.asyncio
    async def test_user_is_create(self, message, async_session):
        await process_start_command(message)

        async with async_session() as session:
            result = await session.scalars(
                select(User).where(User.tg_id == message.from_user.id)
            )
            assert result.one_or_none()
