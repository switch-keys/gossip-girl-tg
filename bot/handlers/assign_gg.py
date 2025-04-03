from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.utils import keyboards
from bot.utils.role_filter import RequireRole
from bot.utils.private_only import PrivateOnly
from api import gossip_girl
from bot.states.assign_gg import AssignGG
from db.model import Role

router = Router()

@router.message(Command("assign_gg"), RequireRole([Role.ADMIN]), PrivateOnly())
async def set_gg_start(message: types.Message, state: FSMContext):
    print("✅ Assign GG handler fired")
    characters = await gossip_girl.list_characters()

    if not characters:
        await message.answer("No users found to assign. Drama-free, for now.")
        return

    await state.set_state(AssignGG.waiting_for_selection)
    await message.answer("Choose your Gossip Girl... 💋", reply_markup=keyboards.assign_gg_select(characters))
