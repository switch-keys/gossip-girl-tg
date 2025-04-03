from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from db.crud import get_db
from db.model import Role

class RequireRole(BaseFilter):
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        telegram_id = event.from_user.id
        async with get_db() as db:
            character = await db.Characters.GetByTelegramId(telegram_id)
            return character and character.role in self.allowed_roles