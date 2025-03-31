from aiogram.fsm.state import StatesGroup, State

class Nickname(StatesGroup):
    waiting_for_target = State()
    waiting_for_input = State()