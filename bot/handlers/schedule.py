from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.utils.role_filter import RequireRole
from db.model import Role
from api import gossip_girl
from zoneinfo import ZoneInfo
from datetime import timedelta
from bot.utils import render, keyboards
from bot.utils.private_only import PrivateOnly

LOCAL_TIMEZONE = ZoneInfo("America/Denver")

router = Router()

@router.message(Command("schedule"), RequireRole([Role.GOSSIP_GIRL, Role.ADMIN]), PrivateOnly())
async def show_schedule(message: Message):
    scheduled = await gossip_girl.list_scheduled()

    if not scheduled:
        await message.answer("No blasts scheduled. The silence is... suspicious 👀")
        return

    text = "<b>🗓️ Scheduled Blasts:</b>\n\n"

    for sub in scheduled:
        mountain_time = sub.scheduled_at - timedelta(hours=6)
        time_str = mountain_time.strftime("%Y-%m-%d %I:%M %p MDT")  # No timezone label

        preview = sub.gg_voice_final or sub.message or "No content"
        snippet = preview[:200] + ("..." if len(preview) > 200 else "")
        text += f"🕒 <b>{time_str}</b>\n<i>{snippet}</i>\n\n"

    await message.answer(
        text,
        reply_markup=keyboards.exit(),
        parse_mode="HTML"
    )
    await message.delete()