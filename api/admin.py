from db.model import Character, Role
from db.crud import get_db

async def assign_gg(telegram_id: int) -> tuple[Character, Character]:
    async with get_db() as db:

        old_gg = await db.Characters.GetGossipGirl()
        new_gg = await db.Characters.GetByTelegramId(telegram_id=telegram_id)
        
        if old_gg:
            old_gg.role = Role.PUBLIC
            await db.Characters.Update(old_gg)

        new_gg.role = Role.GOSSIP_GIRL
        await db.Characters.Update(new_gg)

        return old_gg, new_gg