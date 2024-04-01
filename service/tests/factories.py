from typing import Optional
from dataclasses import dataclass, field

import factory

from database.models import Course


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
    answers: list[str] = field(default_factory=list) 

    async def answer(self, text: str, *args, **kwargs):
        self.answers.append(text)


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


class CourseFactory(factory.Factory):
    class Meta:
        model = Course

    name = factory.Faker("name")
