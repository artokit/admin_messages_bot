from aiogram.fsm.state import StatesGroup, State


class AutoMessages(StatesGroup):
    ask_want_earn = State()
    ask_to_join = State()


class AdminHelp(StatesGroup):
    message_to_admin = State()
