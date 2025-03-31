from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.states.registration import Registration
from db.crud import get_db
from bot.utils import nickname_cache
from bot.utils.commands import set_role_commands
from api import public

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    db = await get_db()
    user = await db.Characters.GetByTelegramId(message.from_user.id)

    if user:
        # Already registered — silently skip or send a friendly message
        await message.answer(f"Looks like you’re already in the game, {user.nickname}. Don’t worry, your secrets are safe... for now. 💋")
        await state.clear()
        return

    await state.set_state(Registration.waiting_for_display_name)
    await message.answer("Welcome to the Gossip Girl game! 💋\n\nPlease enter your full name.")

@router.message(Registration.waiting_for_display_name)
async def handle_display_name(message: types.Message, state: FSMContext):
    await state.update_data(display_name=message.text)
    await state.set_state(Registration.waiting_for_nickname)
    await message.answer("Great. Now enter your nickname (like 'S' or 'Queen B').")

@router.message(Registration.waiting_for_nickname)
async def handle_nickname(message: types.Message, state: FSMContext):
    data = await state.get_data()
    display_name = data.get("display_name")
    nickname = message.text

    character = await public.register(message.from_user.id, message.from_user.username, display_name,
                          nickname)
    await nickname_cache.get_nickname_map(force_reload=True)
    if character:
        await set_role_commands(message.bot, character.telegram_id, role=character.role)
        await message.answer(f"You’re now part of the inner circle, {nickname}. XOXO, Gossip Girl 💋")
    else:
        await message.answer(f"Sorry, {nickname} is already taken. Pick something else — you’re too original to copy. 😉")
    await state.clear()