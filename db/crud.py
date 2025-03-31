from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.database import AsyncSessionLocal
from db.model import Character, Submission, Status, Role
from typing import List

class DB:
    def __init__(self, session):
        self.Characters = Characters(session)
        self.Submissions = Submissions(session)
async def get_db() -> DB:
    async with AsyncSessionLocal() as session:
        db = DB(session)
    return db


#Characters
class Characters:
    def __init__(self, session : AsyncSession):
        self.session = session

    async def Create(self, character: Character) -> bool:
        self.session.add(character)
        try:
            await self.session.commit()
            return True
        except:
            return False
    
    async def GetByTelegramId(self, telegram_id: int) -> Character:
        result = await self.session.execute(select(Character).where(Character.telegram_id == telegram_id))
        return result.scalars().first()
    
    async def GetGossipGirl(self) -> Character:
        result = await self.session.execute(select(Character).where(Character.role == Role.GOSSIP_GIRL))
        return result.scalars().first()
    
    async def ListAll(self) -> List[Character]:
        result = await self.session.execute(select(Character))
        return result.scalars().all()
    
    async def Update(self, character_update: Character) -> Character:
        result = await self.session.execute(select(Character).where(Character.telegram_id == character_update.telegram_id))
        character = result.scalars().first()

        if character:
            character.nickname = character_update.nickname
            character.role = character_update.role

        await self.session.commit()
        await self.session.refresh(character)

        return character

#Submissions
class Submissions:
    def __init__(self, session : AsyncSession):
        self.session = session

    async def Create(self, submission: Submission) -> bool:
        self.session.add(submission)
        await self.session.commit()
        return True
    
    async def GetById(self, id: int) -> Submission:
        result = await self.session.execute(select(Submission).where(Submission.id == id))
        return result.scalars().first()
    
    async def ListPending(self) -> List[Submission]:
        result = await self.session.execute(select(Submission).where(Submission.status == Status.PENDING))
        return result.scalars().all()
    
    async def ListScheduled(self) -> List[Submission]:
        result = await self.session.execute(select(Submission).where(Submission.status == Status.SCHEDULED))
        return result.scalars().all()

    async def ListBySubmitterId(self, submitter_id: int) -> List[Submission]:
        result = await self.session.execute(select(Submission).where(Submission.submitter_id == submitter_id))
        return result.scalars().all()
    
    async def Update(self, submission_update: Submission) -> Submission:
        result = await self.session.execute(select(Submission).where(Submission.id == submission_update.id))
        submission = result.scalars().first()
        if submission:
            submission.reviewer_id = submission_update.reviewer_id
            submission.gg_voice_previous = submission_update.gg_voice_previous
            submission.gg_voice_final = submission_update.gg_voice_final
            submission.is_altered = submission_update.is_altered
            submission.status = submission_update.status
            submission.posted_at = submission_update.posted_at

        await self.session.commit()
        await self.session.refresh(submission)

        return submission
    