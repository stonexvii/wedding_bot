from aiogram.types import Message

from database.tables import QuestionsTable, AnswersTable
from database.requests import get_question, get_user, user_next_question_id


class Answer:

    def __init__(self, answer_id: int, answer_text: str):
        self.id = answer_id
        self.text = answer_text

    def __str__(self):
        return self.text


class Question:

    def __init__(self, question: QuestionsTable, answers: list[AnswersTable]):
        self.id = question.id
        self.text = question.question
        self.video_id = question.video_id
        self.answers = {answer.answer_id: Answer(answer.answer_id, answer.answer) for answer in
                        sorted(answers, key=lambda x: x.id, reverse=True)}

    @classmethod
    async def from_db(cls, question_id: int):
        response = await get_question(question_id)
        if response:
            return cls(*response)

    def __iter__(self):
        return self

    def __next__(self):
        if self.answers:
            return self.answers.popitem()[1]
        raise StopIteration

    def __str__(self):
        return self.text


class User:
    def __init__(self, user_tg_id: int, username: str):
        self.tg_id = user_tg_id
        self.username = username

    @classmethod
    async def from_db(cls, message: Message):
        response = await get_user(message)
        return cls(user_tg_id=response.id, username=response.username)

    @property
    async def next_question_id(self):
        response = await user_next_question_id(self.tg_id)
        return max(response) + 1 if response else 0

    def __str__(self):
        return f'{self.tg_id} ({self.username})'
