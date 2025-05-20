from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import MessageEntityType

import pandas as pd

from classes.classes import Question
from database.requests import next_user_question_id, all_questions, all_answers
from keyboards.keyboards import ikb_answers

from e_sender.email_sender import send_mail

import config

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    question_id = await next_user_question_id(message.from_user.id)
    question = await Question.from_db(question_id)
    if question:
        message_text = question.text
        keyboard = ikb_answers(question)
    else:
        message_text = 'ТЫ УЖЕ ПРИГЛАШЕН! ЗАЕБАЛ!'
        keyboard = None
    await message.answer(
        text=message_text,
        reply_markup=keyboard,
    )


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
