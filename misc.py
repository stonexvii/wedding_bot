from datetime import datetime


def now_timestamp():
    current_time = datetime.now()
    return current_time.strftime('%H:%M:%S %d/%m/%Y')


def on_start():
    print('=' * 60 + f'\nBot is started at {now_timestamp()}!\n' + '=' * 60)


def on_shutdown():
    print('=' * 60 + f'\nBot is shutdown at {now_timestamp()}...\n' + '=' * 60)


def save_message(path: str, message: str):
    with open(path + '.txt', 'w', encoding='UTF-8') as file:
        file.write(message)


def load_message(path: str) -> str:
    with open(path + '.txt', 'r', encoding='UTF-8') as file:
        return file.read()
