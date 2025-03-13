from collections import namedtuple
from random import shuffle

Answers = namedtuple('Answers', ['id', 'text'])


class QuestData:

    def __init__(self, data: dict[int, dict[str, str | dict[int, str]]]):
        self.data = data

    def get_question(self, idx: int) -> str:
        return self.data[idx]['quest']

    def get_answers(self, idx: int) -> list[Answers]:
        result = [Answers(idx, text) for idx, text in self.data[idx]['answers'].items()]
        shuffle(result)
        return result
