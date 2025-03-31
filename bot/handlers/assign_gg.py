from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.utils import keyboards
from api import gossip_girl
from bot.states.assign_gg import AssignGG

router = Router()

@router.message(Command("assign_gg"))
async def set_gg_start(message: types.Message, state: FSMContext):
    characters = await gossip_girl.list_characters()

    if not characters:
        await message.answer("No users found to assign. Drama-free, for now.")
        return

    await state.set_state(AssignGG.waiting_for_selection)
    await message.answer("Choose your Gossip Girl... 💋", reply_markup=keyboards.assign_gg_select(characters))
