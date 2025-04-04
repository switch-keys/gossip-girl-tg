import os
from db.model import Character, Submission, Role, Status, Pronouns
from db.crud import get_db
from api.gpt import gg_voice
from typing import List
from bot.utils.nickname_cache import get_nickname_map

#Register
async def register(telegram_id: int, username: str, display_name: str, nickname: str, pronouns: Pronouns) -> Character:
    async with get_db() as db:
        character = await db.Characters.GetByTelegramId(telegram_id)
        if not character:
            role = Role.PUBLIC
            admins = os.getenv("ADMINS").split(",")
            if str(telegram_id) in admins:
                role = Role.ADMIN
            new_character = Character(telegram_id=telegram_id, username=username, nickname=nickname,
                                    display_name=display_name, role=role, pronouns=pronouns)
            
            await db.Characters.Create(character=new_character)

        return new_character

#Submit Gossip
async def submit(telegram_id: int, msg: str) -> Submission:
    async with get_db() as db:
        nickname_map = await get_nickname_map()
        character = await db.Characters.GetByTelegramId(telegram_id)
        voice = await gg_voice(message=msg, name_map=nickname_map)
        submission = Submission(
            submitter_id=telegram_id,
            submitter_name=character.display_name,
            message=msg,
            gg_voice_original=voice,
            gg_voice_final=voice,
            gg_voice_previous=voice,
            is_altered=False,
            status=Status.PENDING)
        result = await db.Submissions.Create(submission=submission)
        
        return result

#My Gossip
async def list_my_gossip(telegram_id: int) -> List[Submission]:
    async with get_db() as db:
        gossip = db.Submissions.ListBySubmitterId(submitter_id=telegram_id)

        return gossip