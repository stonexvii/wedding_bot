from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.classes import Question
from .callback_data import QuestionCB


def ikb_answers(question: Question):
    keyboard = InlineKeyboardBuilder()
    for answer in question:
        keyboard.button(
            text=answer.text,
            callback_data=QuestionCB(
                button='user_choice',
                question_id=question.id,
                answer_id=answer.id,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()
