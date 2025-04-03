from aiogram.fsm.state import StatesGroup, State

class Bypass(StatesGroup):
    waiting_for_gossip = State()
