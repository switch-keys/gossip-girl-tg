from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.states.registration import Registration
from db.crud import get_db
from db.model import Pronouns
from bot.utils import nickname_cache
from bot.utils.commands import set_role_commands
from api import public
from bot.utils.private_only import PrivateOnly
from bot.utils import keyboards

router = Router()

@router.message(Command("start"), PrivateOnly())
async def start_handler(message: types.Message, state: FSMContext):
    print("✅ Start handler fired")
    async with get_db() as db:
        character = await db.Characters.GetByTelegramId(message.from_user.id)

        if character:
            # Already registered — silently skip or send a friendly message
            await message.answer(f"Looks like you’re already in the game, {character.nickname}. Don’t worry, your secrets are safe... for now. 💋")
            await state.clear()
            return
        await state.update_data(username=message.from_user.username)
        await state.set_state(Registration.waiting_for_display_name)
        await message.answer("Welcome to the Gossip Girl game! 💋\n\nPlease enter your full name.")

@router.message(Registration.waiting_for_display_name)
async def handle_display_name(message: types.Message, state: FSMContext):
    print("✅ Start display name FSM state fired")
    await state.update_data(display_name=message.text)
    await state.set_state(Registration.waiting_for_nickname)
    await message.answer("Great. Now enter your nickname (like 'S' or 'Queen B').")

@router.message(Registration.waiting_for_nickname)
async def handle_nickname(message: types.Message, state: FSMContext):
    print("✅ Start nickname FSM state fired")
    await state.update_data(nickname=message.text)
    await state.update_data(telegram_id=message.from_user.id)
    # await state.set_state(Registration.waiting_for_pronouns)
    keyboard = keyboards.pronouns()
    await message.answer("Last step: select your pronouns", reply_markup=keyboard)

# @router.message(Registration.waiting_for_pronouns)
# async def handle_pronouns(message: types.Message, state: FSMContext):
#     print("Start pronoun FSM state fired")
    
@router.callback_query(F.data.startswith("pronouns:"))
async def handle_pronouns(callback: types.CallbackQuery, state: FSMContext):
    value = callback.data.split(":")[1]
    pronouns = Pronouns[value]
    data = await state.get_data()
    display_name = data.get("display_name")
    username = data.get("username")
    nickname = data.get("nickname")
    telegram_id = data.get("telegram_id")
    try:
        character = await public.register(telegram_id, username, display_name,
                          nickname, pronouns)
    except:
        await callback.message.answer("Error creating character")
    await nickname_cache.get_nickname_map(force_reload=True)
    if character:
        await set_role_commands(callback.message.bot, character.telegram_id, role=character.role)
        await callback.message.answer(f"You’re now part of the inner circle, {nickname}. XOXO, Gossip Girl 💋")
    else:
        await callback.message.answer(f"Sorry, {nickname} is already taken. Pick something else — you’re too original to copy. 😉")
    await callback.message.delete()
    await state.clear()
