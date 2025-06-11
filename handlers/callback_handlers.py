from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from classes.classes import Question
from database.requests import add_user_answer, destruction_of_the_user
from keyboards.keyboards import ikb_answers
from keyboards.callback_data import QuestionCB, ResetConfirm
import misc
from .fsm_states import StartTest

callback_router = Router()


@callback_router.callback_query(QuestionCB.filter(F.button == 'user_choice'), StartTest.wait_question)
async def get_user_choice(callback: CallbackQuery, callback_data: QuestionCB, bot: Bot, state: FSMContext):
    if callback_data.question_id:
        await add_user_answer(callback.from_user.id, callback_data.question_id, callback_data.answer_id)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )
    question_id = callback_data.question_id + 1
    question = await Question.from_db(question_id)
    if not question:
        question = await Question.from_db(100)
        question.text = misc.load_message('outro')
        await state.clear()
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


@callback_router.callback_query(ResetConfirm.filter(F.button == 'confirm'))
async def confirm_reset(callback: CallbackQuery, callback_data: ResetConfirm, bot: Bot):
    await destruction_of_the_user(callback.from_user.id, callback_data.user_id)
    await callback.answer(
        text=f'Пользователь {callback_data.user_id} сброшен!',
        show_alert=True,
    )
    await bot.send_message(
        chat_id=callback_data.user_id,
        text=f'Твои ответы сброшены!\nИспользуй команду /start и проходи тест заново!',
    )
