from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.model import Role
from db.crud import get_db
from api.gpt import verify_gossip
from api.public import submit
from bot.utils.nickname_cache import get_nickname_map
from bot.utils.private_only import PrivateOnly
from bot.utils.role_filter import RequireRole
from bot.utils import render
from bot.utils import keyboards
from bot.states.bypass import Bypass

router = Router()

@router.message(Command("bypass"), RequireRole([Role.ADMIN]), PrivateOnly())
async def handle_message(message: types.Message, state: FSMContext):
    await state.set_state(Bypass.waiting_for_gossip)
    await message.answer("Drop the gossip, darling.")

@router.message(Bypass.waiting_for_gossip)
async def handle_bypass_submission(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id

    # Now that we know they're registered, classify & respond
    name_map = await get_nickname_map()
    response_text, is_gossip = await verify_gossip(message.text,name_map)

    if is_gossip:
        submission = await submit(telegram_id, message.text)
        # Save submission ID in FSM context (optional for tracking across steps)
        await state.update_data(submission_id=submission.id)

        text = render.submission(submission)
        keyboard = keyboards.review(submission.id)

        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer(response_text)
        await state.clear()