from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command
from aiogram.enums import ChatAction

from random import choice

from classes import TestData, User
from data_base import DataBase
from keyboards.callback_data import QuestionCB
from keyboards.keyboards import ikb_start, ikb_answers
# from questions import questions, answers
import text

main_router = Router()
db = DataBase()


async def bot_typing(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,

    )


@main_router.message(Command('start'))
async def com_start(message: Message, bot: Bot):
    await bot_typing(message, bot)
    user = User(message.from_user.id)
    test = TestData(message.from_user.id)
    keyboard = ikb_start()
    message_text = text.greetings_text
    photo = test.start_photo
    if current_id := user.current_question():
        if next_question := test.next_question(current_id):
            keyboard = ikb_answers(next_question)
            message_text = next_question.text
            photo = next_question.photo
        else:
            keyboard = None
            message_text = text.final_text
            photo = test.finish_photo
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=message_text,
        reply_markup=keyboard,
    )
    pass_message = 0
    for idx in range(message.message_id, -1, -1):
        try:
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=idx,
            )
            pass_message = 0
        except:
            pass_message += 1
            if pass_message > 5:
                break
            pass


@main_router.callback_query(QuestionCB.filter())
async def catch_user_answer(callback: CallbackQuery, callback_data: QuestionCB, bot: Bot):
    test = TestData(callback.from_user.id)
    message_prefix = ''
    if callback_data.question_id:
        db.add_answer(callback.from_user.id, callback_data.question_id, callback_data.answer_id)
        message_prefix = f'{choice(text.answers)}\n'
    if next_question := test.next_question(callback_data.question_id):
        message_prefix += 'Следующий вопрос:\n\n'
        photo = InputMediaPhoto(
            media=next_question.photo,
            caption=message_prefix + next_question.text,
        )
    else:
        photo = InputMediaPhoto(
            media=test.photo,
            caption=message_prefix + text.final_text,
        )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=photo,
        reply_markup=ikb_answers(next_question) if next_question else None,
    )


@main_router.message(F.photo)
async def catch_photo(message: Message, bot: Bot):
    if message.caption:
        try:
            db.add_photo(message.from_user.id, int(message.caption), message.photo[-1].file_id)
        except:
            print('ЖОПА!')


@main_router.message()
async def other_massages(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
