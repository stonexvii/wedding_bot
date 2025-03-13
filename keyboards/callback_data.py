from aiogram.filters.callback_data import CallbackData


class QuestionCB(CallbackData, prefix='QCB'):
    question_id: int
    answer_id: int
