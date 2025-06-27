from .commands import command_router
from .callback_handlers import callback_router
from .ya_handlers import yadisk_router

handlers = [
    yadisk_router,
    command_router,
    callback_router,
]
