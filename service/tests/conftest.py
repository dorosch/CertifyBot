import pytest_asyncio
from pytest_factoryboy import register
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy_helpers.aio import get_or_create

from settings import DATABASE_URL
from database.models import User

from .factories import UserFactory, MessageFactory, CourseFactory

register(UserFactory)
register(MessageFactory)
register(CourseFactory)


@pytest_asyncio.fixture(scope="function")
async def async_session():
    """
    An asynchronous session begins a transaction and all records to 
    the database will be rolled back after the test is completed.
    """

    engine = create_async_engine(DATABASE_URL)

    connection = await engine.connect()
    transaction = await connection.begin()

    yield async_sessionmaker(
        bind=connection, expire_on_commit=False, autoflush=False, autocommit=False
    )

    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def isolation(mocker, async_session):
    """Database write isolation level for application."""

    for path in ("main.async_session", "database.models.course.async_session"):
        mocker.patch(path, return_value=async_session())


@pytest_asyncio.fixture(scope="function")
async def user(async_session, user_factory):
    async with async_session() as session:
        async with async_session() as session:
            user = user_factory.create()
            instance, _ = await get_or_create(
                session,
                User,
                tg_id=user.tg_id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                language_code=user.language_code
            )
            await session.commit()

        return instance
