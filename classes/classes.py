from aiogram.types import Message
import yadisk

import config
from database.tables import QuestionsTable, AnswersTable
from database.requests import get_question, get_user, user_next_question_id
from .enums_classes import Extensions, BotPaths


class Answer:

    def __init__(self, answer_id: int, answer_text: str):
        self.id = answer_id
        self.text = answer_text

    def __str__(self):
        return self.text


class Question:

    def __init__(self, question: QuestionsTable, answers: list[AnswersTable]):
        self.id = question.id
        self.text = f'Вопрос {self.id}/10\n{question.question}'
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

    def __next__(self) -> Answer:
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


class YaDisk:
    separator = '/'
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.client = yadisk.AsyncClient(token=config.YADISK_TOKEN)
        self.work_dir = self._join_path(BotPaths.ROOT_DIR.value, BotPaths.GUEST_DIR.value)

    @staticmethod
    def _join_path(*args):
        joined_path = YaDisk.separator.join(args)
        if not joined_path.startswith(YaDisk.separator):
            joined_path = YaDisk.separator + joined_path
        return joined_path

    def _file_name(self, message: Message, file_extension: Extensions):
        new_file_name = BotPaths.FILE_NAME.value.format(user=message.from_user.id,
                                                        number=message.message_id,
                                                        ext=file_extension.value)
        full_path = self._join_path(self.work_dir, new_file_name)
        return full_path

    async def upload(self, file, file_extension: Extensions, message: Message):
        file_path = self._file_name(message, file_extension)
        async with self.client:
            await self.client.upload(file, file_path, timeout=300, retry_interval=30, n_retries=10)
