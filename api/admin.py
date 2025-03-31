from sqlalchemy.future import select
from db.model import Character, Submission, Status, Role
from typing import List
from db.crud import get_db
from gpt import edit_message
from datetime import datetime, timezone

async def assign_gg(telegram_id: int) -> bool:
    db = await get_db()

    old_gg = await db.Characters.GetGossipGirl()
    new_gg = await db.Characters.GetByTelegramId(telegram_id=telegram_id)
    
    old_gg.role = Role.PUBLIC
    new_gg.role = Role.GOSSIP_GIRL

    await db.Characters.Update(old_gg)
    await db.Characters.Update(new_gg)

    return True