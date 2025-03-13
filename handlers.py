from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command
from aiogram.enums import ChatAction

from random import choice

from classes import QuestData
from data_base import DataBase
from keyboards.callback_data import QuestionCB
from keyboards.keyboards import ikb_start, ikb_answers
from questions import questions, answers

main_router = Router()
db = DataBase()


@main_router.message(Command('start'))
async def com_start(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,

    )
    for i in range(message.message_id, message.message_id-20, -1):
        try:
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=i,
            )
        except:
            pass

    answer = QuestData(questions)
    response = db.get_answers(message.from_user.id)
    keyboard = ikb_start()
    message_text = 'Надо пройти тест'
    photo = db.get_photo(1)
    if response:
        current_question_id = max(response)[0]
        keyboard = ikb_answers(current_question_id + 1)
        message_text = answer.get_question(current_question_id + 1)
        photo = db.get_photo(current_question_id + 1)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=message_text,
        reply_markup=keyboard,
    )


@main_router.callback_query(QuestionCB.filter())
async def catch_answer(callback: CallbackQuery, callback_data: QuestionCB, bot: Bot):
    data = QuestData(questions)
    message_prefix = ''
    if callback_data.question_id:
        db.add_answer(callback.from_user.id, callback_data.question_id, callback_data.answer_id)
        message_prefix = f'{choice(answers)}\nСледующий вопрос:\n\n'
    photo = InputMediaPhoto(
        media=db.get_photo(callback_data.question_id + 1),
        caption=message_prefix + data.get_question(callback_data.question_id + 1),
    )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=photo,
        reply_markup=ikb_answers(callback_data.question_id + 1),
    )


@main_router.message(F.photo)
async def catch_photo(message: Message, bot: Bot):
    db.add_photo(message.photo[-1].file_id)
    print(db.get_photo(1))


@main_router.message()
async def other_massages(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
