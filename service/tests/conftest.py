from typing import Optional
from dataclasses import dataclass

import pytest
import pytest_asyncio
from pytest_factoryboy import register
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .factories import UserFactory, MessageFactory
from settings import DATABASE_URL

register(UserFactory)
register(MessageFactory)


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
    # Database write isolation level for application
    mocker.patch("main.async_session", return_value=async_session())
