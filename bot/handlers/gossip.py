from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from db.crud import get_db
from api.gpt import verify_gossip
from api.public import submit

router = Router()

@router.message()
async def handle_message(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        return
    telegram_id = message.from_user.id
    db = await get_db()
    user = await db.Characters.GetByTelegramId(telegram_id)

    if not user:
        await message.answer(
            "Darling, you can’t spill tea if you’re not even invited to the party. "
            "Send /start to get registered. 💋"
        )
        return

    # Now that we know they're registered, classify & respond
    response_text, is_gossip = await verify_gossip(message.text)

    if is_gossip:
        await submit(telegram_id, response_text)
        try:
            await message.delete()
        except Exception as e:
            print(f"Failed to delete gossip message: {e}")

    await message.answer(response_text)