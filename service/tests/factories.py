from typing import Optional
from dataclasses import dataclass

import factory


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
    text_answer: Optional[str] = None

    async def answer(self, text: str):
        self.text_answer = text


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
