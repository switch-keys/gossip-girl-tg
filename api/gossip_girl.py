from sqlalchemy.future import select
from db.model import Character, Submission, Status
from typing import List
from db.crud import get_db
from api.gpt import edit_message as edit_gg_voice
from bot.utils.nickname_cache import get_nickname_map
from datetime import datetime, timezone

async def list_characters() -> List[Character]:
    async with get_db() as db:
        return await db.Characters.ListAll()

async def list_pending() -> List[Submission]:
    async with get_db() as db:
        return await db.Submissions.ListPending()

async def list_scheduled() -> List[Submission]:
    async with get_db() as db:
        return await db.Submissions.ListScheduled()

async def get_submission(submission_id: int) -> Submission:
    async with get_db() as db:
        return await db.Submissions.GetById(submission_id)

async def skip(submission_id: int, reviewer_id: int) -> bool:
    async with get_db() as db:
        submission = await db.Submissions.GetById(submission_id)

        submission.reviewer_id = reviewer_id
        submission.status = Status.SKIPPED

        result = await db.Submissions.Update(submission)
        return result
    
async def schedule(submission_id: int, reviewer_id: int, at_time: datetime) -> bool:
    async with get_db() as db:
        submission = await db.Submissions.GetById(submission_id)

        submission.status = Status.SCHEDULED
        submission.reviewer_id = reviewer_id
        submission.scheduled_at = at_time

        result = await db.Submissions.Update(submission)
        return result

async def blast(submission_id: int) -> bool:
    async with get_db() as db:
        submission = await db.Submissions.GetById(submission_id)

        submission.status = Status.BLASTED
        submission.posted_at = datetime.now(timezone.utc)

        result = await db.Submissions.Update(submission)
        return result

async def edit_message(submission_id: int, prompt: str) -> str:
    async with get_db() as db:
        nickname_map = await get_nickname_map()
        submission = await db.Submissions.GetById(submission_id)
        updated_message = await edit_gg_voice(submission.gg_voice_final, prompt, nickname_map)

        submission.gg_voice_previous = submission.gg_voice_final
        submission.gg_voice_final = updated_message
        submission.is_altered = True

        await db.Submissions.Update(submission)
        return submission.gg_voice_final

async def undo_edit(submission_id: int) -> str:
    async with get_db() as db:
        submission = await db.Submissions.GetById(submission_id)

        submission.gg_voice_final = submission.gg_voice_previous
        submission.is_altered = (submission.gg_voice_final != submission.gg_voice_original)

        await db.Submissions.Update(submission)
        return submission

async def edit_nickname(telegram_id: int, nickname: str) -> bool:
    async with get_db() as db:
        character = await db.Characters.GetByTelegramId(telegram_id=telegram_id)
        character.nickname = nickname

        await db.Characters.Update(character)

        return True