from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from database.requests import get_question

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message):
    for i in range(1, 10):
        response = await get_question(i)
        message_text = f'{response.question}\n{response.answer_1}\n{response.answer_2}\n{response.answer_3}\n{response.answer_4}\n{response.answer_5}\n{response.answer_6}'
        await message.answer(
            text=message_text,
        )
