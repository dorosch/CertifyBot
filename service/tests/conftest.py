from typing import Optional
from dataclasses import dataclass

import pytest
import factory
import factory.fuzzy


@dataclass
class User:
    tg_id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]


@dataclass
class Message:
    from_user: User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    tg_id = factory.fuzzy.FuzzyInteger(1)
    first_name = factory.fuzzy.FuzzyText()
    last_name = factory.fuzzy.FuzzyText()
    username = factory.fuzzy.FuzzyText()
    language_code = factory.fuzzy.FuzzyText()


class MessageFactory(factory.Factory):
    class Meta:
        model = Message

    from_user = factory.SubFactory(UserFactory)


@pytest.fixture(scope="function")
def message() -> Message:
    return MessageFactory()
