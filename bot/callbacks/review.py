from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ForceReply
import asyncio
from api import gossip_girl
from bot.utils import render, keyboards, review_flow
from bot.states.review import Review  # will define next
from bot.utils.delete_message import delete_with_delay

router = Router()

@router.callback_query(F.data.startswith("review:"))
async def handle_review_action(callback: CallbackQuery, state: FSMContext):
    print("✅ Review (Initial) callback fired")
    parts = callback.data.split(":")
    action, submission_id = parts[1], int(parts[2])

    if action == "skip":
        await gossip_girl.skip(submission_id, callback.from_user.id)
        await callback.message.edit_text("Submission skipped. Moving on... 💅")
        asyncio.create_task(delete_with_delay([callback.message], 5))
        await review_flow.send_next_submission(callback.message, state)

    elif action == "schedule":
        await state.update_data(submission_id=submission_id)
        await state.set_state(Review.waiting_for_schedule_delay)
        await callback.message.edit_text("How many minutes from now should this be blasted? ⏰")
        asyncio.create_task(delete_with_delay([callback.message], 3))

    elif action == "edit":
        await state.update_data(submission_id=submission_id)
        await state.set_state(Review.waiting_for_edit_prompt)
        await callback.message.answer(
            f"{callback.message.text}\n"
            "─────────────────────\n"
            "<b>What would you like to change?</b>\n\n"
            "💡 Suggestions:\n"
            "- Add drama\n"
            "- Make it ominous\n"
            "- Romanticize it\n"
            "- Add flair",
            reply_markup=ForceReply(),
            parse_mode="HTML"
        )
        await callback.message.delete()

@router.callback_query(F.data.startswith("review2:accept_edit:"))
async def handle_accept_edit(callback: CallbackQuery, state: FSMContext):
    print("✅ Review (Accept) callback fired")
    submission_id = int(callback.data.split(":")[2])

    # Reload updated submission
    updated = await gossip_girl.get_submission(submission_id)

    await callback.message.edit_text(
        render.submission(updated),
        reply_markup=keyboards.review(updated.id),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("review2:undo_edit:"))
async def handle_undo_edit(callback: CallbackQuery, state: FSMContext):
    print("✅ Review (Edit) callback fired")
    submission_id = int(callback.data.split(":")[2])
    submission = await gossip_girl.undo_edit(submission_id)

    await callback.message.edit_text(
        f"<b>Edit undone.</b>\n\n{render.submission(submission)}",
        reply_markup=keyboards.review(submission.id),
        parse_mode="HTML"
    )