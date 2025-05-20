from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from classes.classes import Question
from database.requests import add_user_answer
from keyboards.keyboards import ikb_answers
from keyboards.callback_data import QuestionCB

callback_router = Router()


@callback_router.callback_query(QuestionCB.filter(F.button == 'user_choice'))
async def get_user_choice(callback: CallbackQuery, callback_data: QuestionCB, bot: Bot):
    await add_user_answer(callback.from_user.id, callback_data.question_id, callback_data.answer_id)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )
    question_id = callback_data.question_id + 1
    question = await Question.from_db(question_id)
    if question:
        keyboard = ikb_answers(question=question)
        if question.video_id:
            await bot.send_video(
                chat_id=callback.from_user.id,
                video=question.video_id,
                caption=question.text,
                reply_markup=keyboard,
            )
        else:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=question.text,
                reply_markup=keyboard,
            )
