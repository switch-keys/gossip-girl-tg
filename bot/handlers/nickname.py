from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from api import gossip_girl
from bot.states.nickname import Nickname
from bot.utils import keyboards, nickname_cache
from bot.utils.role_filter import RequireRole
from db.model import Role
from bot.utils.private_only import PrivateOnly
import asyncio
from bot.utils.delete_message import delete_with_delay
router = Router()

@router.message(Command("nickname"), RequireRole([Role.ADMIN, Role.GOSSIP_GIRL]), PrivateOnly())
async def nickname_start(message: types.Message, state: FSMContext):
    print("✅ Nickname handler fired")
    await message.delete()
    characters = await gossip_girl.list_characters()

    if not characters:
        await message.answer("No users found to nickname. Suspicious... 👀")
        return

    keyboard = keyboards.edit_nickname(characters)

    await message.answer("Whose nickname are we rewriting? 💅", reply_markup=keyboard)

@router.message(Nickname.waiting_for_input)
async def handle_new_nickname(message: types.Message, state: FSMContext):
    print("✅ Nickname input FSM state fired")
    nickname = message.text.strip()
    data = await state.get_data()
    target_telegram_id = data.get("target_telegram_id")

    if not nickname:
        await message.answer("Nice try. A blank nickname won’t do.")
        return

    await gossip_girl.edit_nickname(telegram_id=target_telegram_id, nickname=nickname)
    await nickname_cache.get_nickname_map(force_reload=True)
    response = await message.answer(f"Nickname updated to <b>{nickname}</b>. XOXO 💋", parse_mode="HTML")
    asyncio.create_task(delete_with_delay([message.reply_to_message,message,response],3))
    await state.clear()
