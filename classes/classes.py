from collections import namedtuple
from random import shuffle

from database.requests import add_question
import text


class Answer:

    def __init__(self, answer_id: int, answer_text: str):
        self.id = answer_id
        self.answer = answer_text

    def __str__(self):
        return self.answer


class Question:

    def __init__(self, question_id: int, question: dict[str, str | dict[int, str]]):
        self.id = question_id
        self.question = question['quest']
        self.answers = {f'answer_{answer_id}': answer_text for answer_id, answer_text in question['answers'].items()}

    # @property
    # def photo(self):
    #     return db.get_photo(self.id, self.id)

    async def save(self):
        data = {'question': self.question}
        data.update(self.answers)
        await add_question(**data)

    def __str__(self):
        return self.question

# class TestData:
#
#     def __init__(self, user_id: int):
#         self.data = text.questions
#         self.questions = {quest_id: Question(quest_id, quest['quest'], quest['answers']) for quest_id, quest in
#                           self.data.items()}
#         self.start_photo = db.get_photo(user_id, 0)
#         self.finish_photo = db.get_photo(user_id, -1)
#
#     def get_question(self, idx: int) -> Question:
#         return self.questions[idx]
#
#     def get_answers(self, idx: int) -> list[Answer]:
#         result = self.questions[idx].answers
#         shuffle(result)
#         return result
#
#     def next_question(self, current_id: int):
#         if current_id < max(self.questions):
#             return self.questions[current_id + 1]
#
#
# class User:
#
#     def __init__(self, user_id: int):
#         self.id = user_id
#
#     def current_question(self):
#         if questions_ids := db.get_user_answers_id(self.id):
#             return max(questions_ids)[0]
