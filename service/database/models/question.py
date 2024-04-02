from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

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


class AnswerHistory(Model):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question = relationship("Question")
    user = relationship("User", backref="answers")

    def __str__(self) -> str:
        return f"{self.id} - Question {self.question_id}"
