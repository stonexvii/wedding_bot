from enum import Enum


class Extensions(Enum):
    PHOTO = 'png'
    VIDEO = 'mp4'


class BotPaths(Enum):
    ROOT_DIR = 'wedding_30_06_25'
    GUEST_DIR = 'guest_media'
    FILE_NAME = '{user}_{number}.{ext}'
