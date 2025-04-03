from api import gossip_girl
from bot.utils import render, keyboards
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.utils.delete_message import delete_with_delay
import asyncio

async def send_next_submission(message: Message, state: FSMContext):
    pending = await gossip_girl.list_pending()

    if not pending:
        response = await message.answer("That’s all for now. No more juicy secrets... yet. 💋")
        asyncio.create_task(delete_with_delay([message,response],5))
        await state.clear()
        return

    next_submission = pending[0]
    await state.update_data(submission_id=next_submission.id)

    await message.answer(
        render.submission(next_submission),
        reply_markup=keyboards.review(next_submission.id),
        parse_mode="HTML"
    )
