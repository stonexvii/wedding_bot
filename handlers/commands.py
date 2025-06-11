from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import MessageEntityType

import pandas as pd

from classes.classes import Question, User
from database.requests import all_questions, all_answers, add_new_question, all_users, user_answers, \
    collect_user_answers, destruction_of_the_user
from keyboards.keyboards import ikb_answers, ikb_confirm_user_clear
import misc
from .fsm_states import NewQuestion, StartTest
from e_sender.email_sender import send_mail

import config

command_router = Router()


@command_router.message(Command('clear'), StartTest.wait_question)
@command_router.message(Command('clear'))
async def clear_user(message: Message, command: CommandObject, bot: Bot):
    if command.args:
        if command.args.isdigit():
            print(f'Удаление {command.args}')
            await destruction_of_the_user(message.from_user.id, int(command.args))
    else:
        await bot.send_message(
            chat_id=config.ADMIN_TG_ID,
            text=f'Обновить пользователя {message.from_user.id}',
            reply_markup=ikb_confirm_user_clear(message.from_user.id),
        )


@command_router.message(StartTest.wait_question)
async def message_cleaner(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )


@command_router.message(Command('start'))
async def command_start(message: Message, bot: Bot, state: FSMContext):
    user = await User.from_db(message)
    next_question_id = await user.next_question_id
    question = await Question.from_db(next_question_id)
    if question:
        if not next_question_id:
            question.text = misc.load_message('intro')
        await state.set_state(StartTest.wait_question)
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
        text='Пришли вопрос и ответы',
    )
    await state.set_state(NewQuestion.question_catch)


@command_router.message(NewQuestion.question_catch)
async def new_question(message: Message, state: FSMContext):
    msg = message.caption if message.video else message.text
    if not (msg.startswith('0') or msg.startswith('100')):
        question_id, question, *answers = msg.split('\n')
        video_id = message.video.file_id if message.video else None
    else:
        question_id, question, *answers = msg.split('\n', 1)
        video_id = message.video.file_id if message.video else None
    await add_new_question(int(question_id), question, answers, video_id)
    await state.clear()


async def create_static_file():
    statistic = {}
    questions = await all_questions()
    questions_data = [await Question.from_db(question.id) for question in questions if question.id]
    for question in questions_data:
        statistic[question.id] = {answer: 0 for answer in question.answers}
        statistic[question.id]['total'] = 0
        statistic[question.id]['question']: Question = question
    result = await all_answers()
    for entry in result:
        if entry.question_id:
            statistic[entry.question_id][entry.answer_id] += 1
            statistic[entry.question_id]['total'] += 1
    file_data = {1: [], 2: []}
    for question, answers in statistic.items():
        current_question = answers['question']
        file_data[1].append(str(current_question))
        file_data[2].append('')

        for answer_id, answer in answers.items():
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
    if message.entities:
        for entity in message.entities:
            if entity.type == MessageEntityType.EMAIL:
                email_address = entity.extract_from(message.text)
                if send_mail(email_address):
                    await message.answer(
                        text=f'Статистика отправлена по адресу {entity.extract_from(message.text)}',
                    )


@command_router.message(Command('statistics'))
async def statistics_command(message: Message):
    result = ''
    questions = await all_questions()
    users = await all_users()
    for user in users:
        result += f'@{user.username}  -  '
        count = await user_answers(user_tg_id=user.id)
        result += f'{len(count)}/{len(questions) - 2}\n'
    await message.answer(
        text=result,
    )


@command_router.message(Command('collect'))
async def collect_user_answers_handler(message: Message, command: CommandObject):
    if command.args:
        response = await collect_user_answers(command.args)
        message_text = f'Ответы пользователя {command.args}\n'
        message_text += '\n\n'.join(['\n'.join(answer) for answer in response])
        await message.answer(
            text=message_text,
        )


@command_router.message(Command('get_id'))
async def get_user_id(message: Message):
    await message.answer(
        text=str(message.from_user.id),
    )


@command_router.message(Command('intro'))
async def intro_message(message: Message, command: CommandObject):
    misc.save_message('intro', command.args)


@command_router.message(Command('outro'))
async def intro_message(message: Message, command: CommandObject):
    misc.save_message('outro', command.args)


@command_router.message(Command('test'))
async def intro_message(message: Message, command: CommandObject):
    await message.answer(
        text='WORK!',
    )
