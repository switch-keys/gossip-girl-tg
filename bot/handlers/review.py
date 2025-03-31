from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.states.review import Review
from api import gossip_girl
from bot.utils import render, keyboards, review_flow
from datetime import datetime, timedelta, timezone

router = Router()

@router.message(Command("review"))
async def review_handler(message: types.Message, state: FSMContext):
    pending = await gossip_girl.list_pending()

    if not pending:
        await message.answer("No more submissions to review. Looks like the drama's on pause. 💅")
        return

    submission = pending[0]  # Pick the first one in the list

    # Save submission ID in FSM context (optional for tracking across steps)
    await state.update_data(submission_id=submission.id)

    text = render.submission(submission)
    keyboard = keyboards.review(submission.id)

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.message(Review.waiting_for_schedule_delay)
async def handle_schedule_delay(message: types.Message, state: FSMContext):
    try:
        minutes = int(message.text.strip())
        if minutes <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("That’s not a valid number of minutes, darling. Try again.")
        return

    data = await state.get_data()
    submission_id = data.get("submission_id")

    # 🔄 Safe, timezone-aware UTC timestamp
    scheduled_time = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    await gossip_girl.schedule(submission_id=submission_id, at_time=scheduled_time)

    await message.answer(f"Scheduled for blast in {minutes} minutes. 🧨")

    await review_flow.send_next_submission(message, state)


@router.message(Review.waiting_for_edit_prompt)
async def handle_edit_guidance(message: types.Message, state: FSMContext):
    guidance = message.text.strip()
    data = await state.get_data()
    submission_id = data.get("submission_id")

    submission = await gossip_girl.edit_message(submission_id=submission_id, prompt=guidance)

    # Save updated gg_voice_final in context if needed
    await state.update_data(edited_submission=submission)

    await message.answer(
        f"<b>Updated Gossip Girl Voice:</b>\n{submission.gg_voice_final}",
        reply_markup=keyboards.edit_message(submission_id),
        parse_mode="HTML"
    )