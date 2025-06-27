import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message

from classes import YaDisk
from classes.enums_classes import Extensions

yadisk_router = Router()


@yadisk_router.message(F.document)
async def main_handler(message: Message, bot: Bot):
    file = await bot.download(message.document.file_id)
    ya_disk = YaDisk()
    await ya_disk.upload(file, Extensions.PHOTO, message)


@yadisk_router.message(F.photo)
async def main_handler(message: Message, bot: Bot):
    file = await bot.download(message.photo[-1].file_id)
    ya_disk = YaDisk()
    await ya_disk.upload(file, Extensions.PHOTO, message)


@yadisk_router.message(F.video)
async def main_handler(message: Message, bot: Bot):
    file = await bot.download(message.video.file_id)
    ya_disk = YaDisk()
    await ya_disk.upload(file, Extensions.VIDEO, message)
