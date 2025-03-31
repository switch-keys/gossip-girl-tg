from aiogram.fsm.state import State, StatesGroup

class Review(StatesGroup):
    waiting_for_schedule_delay = State()
    waiting_for_edit_prompt = State()