from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.classes import Question
# from questions import questions
from .callback_data import QuestionCB


def ikb_start():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Начать',
        callback_data=QuestionCB(
            answer_id=0,
            question_id=0,
        ),
    )
    return keyboard.as_markup()


def ikb_answers(question: Question):
    keyboard = InlineKeyboardBuilder()
    for answer in set(question.answers):
        keyboard.button(
            text=answer.text,
            callback_data=QuestionCB(
                answer_id=answer.id,
                question_id=question.id,
            ),
        )
    keyboard.adjust(2, 2)
    return keyboard.as_markup()
