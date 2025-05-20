from aiogram.fsm.state import State, StatesGroup


class NewQuestion(StatesGroup):
    question_catch = State()
