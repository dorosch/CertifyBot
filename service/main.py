import asyncio
import logging.config
import os

import aiogram.exceptions
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram.types import InlineKeyboardButton
from aiogram.utils.formatting import Text, Bold
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardMarkup
from sqlalchemy import select
from sqlalchemy_helpers.aio import get_or_create

import settings
from database import async_session
from database.models import User, Course, UserCourse

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
class StartCommandHandler(MessageHandler):
    """
    Handler of the start command.

    The start command takes or creates a user and displays a list of 
    available courses for him to start.
    """

    async def handle(self):
        async with async_session() as session:
            await get_or_create(
                session,
                User,
                tg_id=self.from_user.id,
                first_name=self.from_user.first_name,
                last_name=self.from_user.last_name,
                username=self.from_user.username,
                language_code=self.from_user.language_code
            )
            await session.commit()

            courses = await session.scalars(select(Course))

        await self.answer_available_courses(courses.all())

    async def answer_available_courses(self, courses: list[Course]):
        for course in courses:
            await self.event.answer(
                **Text(
                    Bold(course.name),
                    "\n\n",
                    course.description
                ).as_kwargs(),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Start course",
                            callback_data=CourseCallbackData(
                                code=course.code
                            ).pack()
                        )
                    ]
                ])
            )


class CourseCallbackData(CallbackData, prefix="course"):
    code: str


@dispatcher.callback_query(CourseCallbackData.filter())
class CourseCallbackHandler(CallbackQueryHandler):
    """
    Callback for selecting a specific course to start.

    Posting the start command, user selects one from the list of courses and 
    the button for the selected course makes a callback to this class.
    """

    async def handle(self):
        callback_data = CourseCallbackData.unpack(self.callback_data)

        async with async_session() as session:
            course_id = await session.scalar(
                select(Course.id).where(Course.code == callback_data.code)
            )
            user_id = await session.scalar(
                select(User.id).where(User.tg_id == self.event.from_user.id)
            )

        if course_id and user_id:
            await UserCourse.activate(course_id, user_id)
            await self.message.answer("Course has been started!")
        else:
            logger.error(
                "Error activate course=%s for user=%s", course_id, user_id
            )
            await self.message.answer(
                "I can't activate the course, try another one"
            )


async def main():
    logger.info("Application start")

    bot = Bot(token=os.environ["TOKEN"])

    try:
        await dispatcher.start_polling(bot)
    finally:
        try:
            await bot.close()
        except aiogram.exceptions.TelegramRetryAfter as error:
            # There except needed because if you call bot.close()
            # to many telegram will block your calls for 10 minutes
            logger.error(error)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application stopped")
