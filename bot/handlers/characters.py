from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db.crud import get_db

router = Router()

@router.message(Command("characters"))
async def characters_list(message: Message):
    async with get_db() as db:
        users = await db.Characters.ListAll()
        if not users:
            await message.answer("No characters registered yet. The stage is empty... for now.")
            return

        # Sort alphabetically by display name
        users.sort(key=lambda u: u.display_name.lower())

        lines = ["<b>🎭 The Cast of Gossip Girl:</b>\n"]
        for user in users:
            display = user.display_name
            nickname = f'"{user.nickname}"' if user.nickname else ""
            pronouns = f"({user.pronouns.value})" if user.pronouns else ""
            lines.append(f"• {display} → {nickname} {pronouns}")

        await message.answer("\n".join(lines), parse_mode="HTML")