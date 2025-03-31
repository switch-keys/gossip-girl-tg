import os
from db.model import Character, Submission, Role, Status
from db.crud import get_db
from api.gpt import gg_voice
from typing import List
from bot.utils.nickname_cache import nickname_map

#Register
async def register(telegram_id: int, username: str, display_name: str, nickname: str) -> Character:
    db = await get_db()
    character = await db.Characters.GetByTelegramId(telegram_id)
    if not character:
        role = Role.PUBLIC
        if telegram_id in os.getenv("ADMINS").split(","):
            role = Role.ADMIN
        new_character = Character(telegram_id=telegram_id, username=username, nickname=nickname,
                                  display_name=display_name, role=role)
        
        await db.Characters.Create(character=new_character)

    return new_character

#Submit Gossip
async def submit(telegram_id: int, message: str) -> bool:
    db = await get_db()
    gg_voice_original = await gg_voice(message=message, name_map=nickname_map)
    submission = Submission(submitter_id=telegram_id, message=message, gg_voice_original=gg_voice_original,
                            gg_voice_final=gg_voice_original, gg_voice_previous= gg_voice_original,
                            is_altered=False, status= Status.PENDING)
    result = await db.Submissions.Create(submission=submission)
    
    return result

#My Gossip
async def list_my_gossip(telegram_id: int) -> List[Submission]:
    db = await get_db()
    gossip = db.Submissions.ListBySubmitterId(submitter_id=telegram_id)

    return gossip