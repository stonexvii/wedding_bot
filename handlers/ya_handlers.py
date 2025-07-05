from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from classes import YaDisk
from classes.enums_classes import Extensions

yadisk_router = Router()


@yadisk_router.message(F.photo | F.document | F.video)
async def media_data_handler(message: Message, bot: Bot):
    ya_disk = YaDisk()
    if message.photo:
        file_id = message.photo[-1].file_id
        file_ext = Extensions.PHOTO
    elif message.video:
        file_id = message.video.file_id
        file_ext = Extensions.VIDEO
    else:
        file_id = message.document.file_id
        file_ext = Extensions.PHOTO if message.document.mime_type.startswith('image') else Extensions.VIDEO
    try:
        file = await bot.download(file_id)
    except TelegramBadRequest as e:
        await message.answer(text='Размер файла слишком большой!\nОтправьте файл в личку @STONE_XVII для загрузки')
    else:
        await ya_disk.upload(file, file_ext, message)
