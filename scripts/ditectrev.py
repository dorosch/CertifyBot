"""
Importing questions from project readme files https://github.com/Ditectrev.

To use, specify the path to the readme file with questions and run script:
    $ python3 scripts/ditectrev.py questions.md

Warning:
    * Some questions have images, don't forget to copy them to images directory.
    * Questions may contain links to images on a new line, move them to one line.
"""

import argparse
import dataclasses
import re
import sys
import json

QUESTION_REGEX = re.compile("### (?P<question_text>.*?)\n")
ANSWER_REGEX = re.compile("- \[(?P<is_correct>[x ])\] (?P<answer_text>.*?)(?=\n)")


@dataclasses.dataclass
class Answer:
    text: str
    is_correct: bool = False

    @staticmethod
    def parse(match: re.Match) -> "Answer":
        return Answer(
            text=match.group(2),
            is_correct=(match.group(1) == "x")
        )

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "is_correct": self.is_correct
        }


@dataclasses.dataclass
class Question:
    text: str
    answers: list[Answer]

    @staticmethod
    def parse(match: re.Match) -> "Question":
        return Question(
            text=match.group(1),
            answers=[]
        )

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "answers": [
                answer.to_dict() for answer in self.answers
            ]
        }

def main():
    parser = argparse.ArgumentParser(
        description="Import Ditectrev questions"
    )
    parser.add_argument("file_path", type=argparse.FileType("r"), help="Path to the README.md file")
    args = parser.parse_args()

    questions = []

    for line in args.file_path:
        if match := re.search(QUESTION_REGEX, line):
            questions.append(Question.parse(match))
        elif match := re.search(ANSWER_REGEX, line):
            questions[-1].answers.append(Answer.parse(match))

    sys.stdout.write(
        json.dumps([question.to_dict() for question in questions], indent=4)
    )


if __name__ == "__main__":
    main()
