import enum
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Enum, Integer, BigInteger, String, Boolean, ForeignKey, Text, DateTime, func, text

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

class Pronouns(enum.Enum):
    HE = "he/him"
    SHE = "she/her"
    THEY = "they/them"

# Person
class Character(Base):
    __tablename__ = "characters"

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=True)
    nickname = Column(String, nullable=False, unique=True)
    display_name = Column(String, nullable=False)
    role = Column(Enum(Role))
    pronouns = Column(Enum(Pronouns))

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submitter_id = Column(Integer, ForeignKey("characters.telegram_id", ondelete="CASCADE"), nullable=False)
    submitter_name = Column(Text, nullable=False)
    reviewer_id = Column(Integer, ForeignKey("characters.telegram_id", ondelete="SET NULL"), nullable=True)
    message = Column(Text, nullable=False)
    gg_voice_original = Column(Text, nullable=False)
    gg_voice_final = Column(Text, nullable=False)
    gg_voice_previous = Column(Text, nullable=False)
    is_altered = Column(Boolean, nullable=False)
    status = Column(Enum(Status))
    submitted_at = Column(DateTime(timezone=True), server_default=text("(datetime('now'))"))
    scheduled_at = Column(DateTime(timezone=True))
    posted_at = Column(DateTime(timezone=True))