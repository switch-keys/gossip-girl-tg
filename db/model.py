import enum
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Enum, Integer, BigInteger, String, Boolean, ForeignKey, Text, TIMESTAMP, func

Base = declarative_base()

# Role
class Role(enum.Enum):
    ADMIN = "Admin"
    PUBLIC = "Public"
    GOSSIP_GIRL = "Gossip Girl"

class Status(enum.Enum):
    PENDING = "Pending"
    SCHEDULED = "Scheduled"
    BLASTED = "Blasted"
    SKIPPED = "Skipped"

# Person
class Character(Base):
    __tablename__ = "characters"

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    nickname = Column(String, nullable=False, unique=True)
    display_name = Column(String, nullable=False)
    role = Column(Enum(Role))

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submitter_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("characters.id", ondelete="SET NULL"), nullable=True)
    message = Column(Text, nullable=False)
    gg_voice_original = Column(Text, nullable=False)
    gg_voice_final = Column(Text, nullable=False)
    gg_voice_previous = Column(Text, nullable=False)
    is_altered = Column(Boolean, nullable=False)
    status = Column(Enum(Status))
    submitted_at = Column(TIMESTAMP, server_default=func.now())
    posted_at = Column(TIMESTAMP)