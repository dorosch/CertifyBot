from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from .base import Model


class PreviewMixin:
    def preview(self) -> str:
        words = self.text.split()
        preview = " ".join(words[:7])

        if len(words) < 7:
            return preview

        return f"{preview}..."


class Question(PreviewMixin, Model):
    course_id = Column(Integer, ForeignKey("course.id"))
    text = Column(String, nullable=False)
    answers = relationship("Answer", backref="question", lazy=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.preview()}"


class Answer(PreviewMixin, Model):
    question_id = Column(Integer, ForeignKey("question.id"))
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)

    def __str__(self) -> str:
        return f"{self.id} - {self.preview()}"
