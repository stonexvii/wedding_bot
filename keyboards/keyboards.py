from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.classes import Question
from .callback_data import QuestionCB

text_buttons = [
    'A',
    'B',
    'C',
    'D',
]


def ikb_answers(question: Question):
    keyboard = InlineKeyboardBuilder()
    for idx, answer in enumerate(question.answers):
        keyboard.button(
            text=text_buttons[idx] if question.id else answer.text,
            callback_data=QuestionCB(
                button='user_choice',
                question_id=question.id,
                answer_id=answer.id,
            ),
        )
    keyboard.adjust(4)
    return keyboard.as_markup()
