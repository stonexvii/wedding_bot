def on_start():
    print('Bot is started!')


def on_shutdown():
    print('Bot is shutdown...')


def save_message(path: str, message: str):
    with open(path + '.txt', 'w', encoding='UTF-8') as file:
        file.write(message)


def load_message(path: str) -> str:
    with open(path + '.txt', 'r', encoding='UTF-8') as file:
        return file.read()
