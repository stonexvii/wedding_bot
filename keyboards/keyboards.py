from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes import QuestData
from questions import questions
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


def ikb_answers(current_question: int):
    keyboard = InlineKeyboardBuilder()
    answers = QuestData(questions)
    for answer in answers.get_answers(current_question):
        keyboard.button(
            text=answer.text,
            callback_data=QuestionCB(
                answer_id=answer.id,
                question_id=current_question,
            ),
        )
    keyboard.adjust(2, 2)
    return keyboard.as_markup()
