import os
import asyncio

from aiogram import Bot, Dispatcher

import text

from classes.classes import Question

from database.database import create_tables
from database.requests import get_question
from handlers import main_router
from misc import *


async def start_bot():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    await create_tables()
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
