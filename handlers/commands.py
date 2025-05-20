from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import MessageEntityType

import pandas as pd

from classes.classes import Question, User
from database.requests import all_questions, all_answers, add_new_question
from keyboards.keyboards import ikb_answers
from .fsm_states import NewQuestion
from e_sender.email_sender import send_mail

import config

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    user = await User.from_db(message)
    next_question_id = await user.next_question_id
    question = await Question.from_db(next_question_id)
    if question:
        keyboard = ikb_answers(question=question)
        if question.video_id:
            await bot.send_video(
                chat_id=message.from_user.id,
                video=question.video_id,
                caption=question.text,
                reply_markup=keyboard,
            )
        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=question.text,
                reply_markup=keyboard,
            )


@command_router.message(Command('add'))
async def command_add(message: Message, state: FSMContext):
    await message.answer(
        text='Пришли вопрос и ответы'
    )
    await state.set_state(NewQuestion.question_catch)


@command_router.message(NewQuestion.question_catch)
async def new_question(message: Message, state: FSMContext):
    msg = message.caption if message.video else message.text
    question_id, question, *answers = msg.split('\n')
    video_id = message.video.file_id if message.video else None
    await add_new_question(int(question_id), question, answers, video_id)
    await state.clear()


async def create_static_file():
    statistic = {}
    questions = await all_questions()
    questions_data = [await Question.from_db(question.id) for question in questions]
    for question in questions_data:
        statistic[question.id] = {answer: 0 for answer in question.answers}
        statistic[question.id]['total'] = 0
        statistic[question.id]['question']: Question = question
    result = await all_answers()
    for entry in result:
        statistic[entry.question_id][entry.answer_id] += 1
        statistic[entry.question_id]['total'] += 1
    file_data = {1: [], 2: []}
    for question, answers in statistic.items():

        current_question = answers['question']
        file_data[1].append(str(current_question))
        file_data[2].append('')

        for answer_id, answer in answers.items():
            row = []
            if isinstance(answer_id, int):
                file_data[1].append(str(current_question.answers[answer_id]))
                file_data[2].append(f'{round(answer / answers['total'] * 100, 2)}%')
        file_data[1].append('')
        file_data[2].append('')

    df = pd.DataFrame(file_data)
    df.to_excel(config.FILE_NAME_STATIC, index=False)


@command_router.message(Command('send'))
async def send_command(message: Message):
    await create_static_file()
    for entity in message.entities:
        if entity.type == MessageEntityType.EMAIL:
            email_address = entity.extract_from(message.text)
            if send_mail(email_address):
                await message.answer(
                    text=f'Статистика отправлена по адресу {entity.extract_from(message.text)}',
                )
