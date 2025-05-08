from database.tables import QuestionsTable, AnswersTable
from database.requests import get_question


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
        self.answers = {answer.answer_id: Answer(answer.answer_id, answer.answer) for answer in answers}

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
