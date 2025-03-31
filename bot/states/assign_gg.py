from aiogram.fsm.state import StatesGroup, State

class AssignGG(StatesGroup):
    waiting_for_selection = State()
    waiting_for_confirmation = State()
