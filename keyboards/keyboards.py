from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.classes import Question
from .callback_data import QuestionCB, ResetConfirm

text_buttons = [
    'A',
    'B',
    'C',
    'D',
]


def ikb_answers(question: Question):
    keyboard = InlineKeyboardBuilder()
    for idx, answer in enumerate(question):
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


def ikb_confirm_user_clear(user_tg_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Сбросить',
        callback_data=ResetConfirm(
            button='confirm',
            user_id=user_tg_id,
        )
    )
    keyboard.button(
        text='Отменить',
        callback_data=ResetConfirm(
            button='cancel',
            user_id=user_tg_id,
        )
    )
    return keyboard.as_markup()
