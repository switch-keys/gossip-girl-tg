from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    waiting_for_display_name = State()
    waiting_for_nickname = State()