from datetime import datetime


def now_timestamp():
    current_time = datetime.now()
    return current_time.strftime('%H:%M:%S %d/%m/%Y')


def on_start():
    print(f'\n\n\n\n\nBot is started at {now_timestamp()}!\n\n\n\n\n')


def on_shutdown():
    print(f'\n\n\n\n\nBot is shutdown at {now_timestamp()}...\n\n\n\n\n')


def save_message(path: str, message: str):
    with open(path + '.txt', 'w', encoding='UTF-8') as file:
        file.write(message)


def load_message(path: str) -> str:
    with open(path + '.txt', 'r', encoding='UTF-8') as file:
        return file.read()


print(now_timestamp())
