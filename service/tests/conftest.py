from typing import Optional
from dataclasses import dataclass

import pytest
import factory
import factory.fuzzy


@dataclass
class User:
    id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]


@dataclass
class Message:
    from_user: User
    _answer: str = ''

    async def answer(self, text: str):
        self._answer = text

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Faker("pyint")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("pystr")
    language_code = factory.Faker("locale")


class MessageFactory(factory.Factory):
    class Meta:
        model = Message

    from_user = factory.SubFactory(UserFactory)


@pytest.fixture(scope="function")
def message() -> Message:
    return MessageFactory()
