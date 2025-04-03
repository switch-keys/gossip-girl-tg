from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from db.crud import get_db
from api.gpt import verify_gossip
from api.public import submit
from bot.utils.nickname_cache import get_nickname_map
from bot.utils.private_only import PrivateOnly

router = Router()

@router.message(PrivateOnly())
async def handle_message(message: types.Message, state: FSMContext):
    print("✅ Gossip catch all callback fired")
    if message.text.startswith("/"):
        return
    telegram_id = message.from_user.id
    async with get_db() as db:
        user = await db.Characters.GetByTelegramId(telegram_id)

        if not user:
            await message.answer(
                "Darling, you can’t spill tea if you’re not even invited to the party. "
                "Send /start to get registered. 💋"
            )
            return

    # Now that we know they're registered, classify & respond
    name_map = await get_nickname_map()
    response_text, is_gossip = await verify_gossip(message.text,name_map)

    if is_gossip:
        await submit(telegram_id, message.text)

    await message.answer(response_text)