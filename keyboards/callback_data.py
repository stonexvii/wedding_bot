from aiogram.filters.callback_data import CallbackData


class QuestionCB(CallbackData, prefix='QCB'):
    button: str
    question_id: int
    answer_id: int
