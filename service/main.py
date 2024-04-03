import asyncio
import logging.config
import os
from string import ascii_uppercase

import aiogram.exceptions
from aiogram import Bot, Dispatcher, md
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.enums import ParseMode
from sqlalchemy import select
from sqlalchemy_helpers.aio import get_or_create

import settings
from database import async_session
from database.models import User, Course, UserCourse

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

dispatcher = Dispatcher()


class CourseCallbackData(CallbackData, prefix="course"):
    code: str


class QuestionCallbackData(CallbackData, prefix="question"):
    answers: int
    position: int
    is_correct: bool
    course_id: int
    user_id: int


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
                f"*{md.quote(course.name)}*"
                "\n\n"
                f"{md.quote(course.description)}"
                "\n\n"
                f"{md.link('Link to the course', course.link)}",
                parse_mode=ParseMode.MARKDOWN_V2,
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
            await QuestionHelper(self.event).ask(course_id, user_id)
        else:
            logger.error(
                "Error activate course=%s for user=%s", course_id, user_id
            )
            await self.event.answer(
                "I can't activate the course, try another one"
            )

        await self.event.answer()


@dispatcher.callback_query(QuestionCallbackData.filter())
class AnswerCallbackHandler(CallbackQueryHandler):
    async def handle(self):
        keyboard = self.message.reply_markup.inline_keyboard
        callback_data = QuestionCallbackData.unpack(self.callback_data)

        for index, button in enumerate(keyboard[0]):
            if callback_data.position != index:
                continue

            if callback_data.is_correct:
                if not button.text.startswith("✅"):
                    button.text = f"✅ {button.text}"
            else:
                if not button.text.startswith("❌"):
                    button.text = f"❌ {button.text}"

        answers = sum(1 for button in keyboard[0] if button.text.startswith("✅"))
        has_errors = any(True for button in keyboard[0] if button.text.startswith("❌"))

        if has_errors or callback_data.answers == answers:
            # TODO: Write answer result to the AnswerHistory model

            await self.message.edit_text(
                ("❌ " if has_errors else "✅ ") + self.message.md_text,
                parse_mode=ParseMode.MARKDOWN_V2
            )

            if has_errors:
                await self.event.answer("Incorrect")
            else:
                await self.event.answer("Correct")

            await QuestionHelper(self.event).ask(
                callback_data.course_id, callback_data.user_id
            )
        else:
            try:
                await self.message.edit_reply_markup(
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
                )
            except TelegramBadRequest:
                pass

            await self.event.answer()


class QuestionHelper:
    def __init__(self, event: CallbackQuery):
        self.event = event

    async def ask(self, course_id: int, user_id: int):
        question = await Course.next_question(course_id, user_id)

        if not question:
            return await self.event.message.answer(
                "You successfull finished this course!!1"
            )

        text = f"*{md.quote(question.text)}*\n\n"

        for index, answer in enumerate(question.answers):
            text += f"{ascii_uppercase[index]}\) {md.quote(answer.text)}\n\n"

        await self.event.message.answer(
            text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=ascii_uppercase[index],
                        callback_data=QuestionCallbackData(
                            position=index,
                            is_correct=answer.is_correct,
                            answers=sum(1 for a in question.answers if a.is_correct),
                            course_id=course_id,
                            user_id=user_id
                        ).pack()
                    )
                    for index, answer in enumerate(question.answers)
                ]
            ])
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
