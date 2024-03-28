import asyncio
import logging.config
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy_helpers.aio import get_or_create

import settings
from database import async_session
from database.models import User

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def process_start_command(message: Message):
    async with async_session() as session:
        await get_or_create(
            session,
            User,
            tg_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            language_code=message.from_user.language_code
        )
        await session.commit()

    await message.answer('Hi!')


async def main():
    logger.info("start application")

    bot = Bot(token=os.environ["TOKEN"])

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
