import asyncio
from aiogram import Bot
from datetime import datetime, timezone
from api import gossip_girl

BLAST_INTERVAL_SECONDS = 60  # check every minute

async def loop(bot: Bot):
    while True:
        try:
            scheduled = await gossip_girl.list_scheduled()

            for submission in scheduled:
                if submission.scheduled_at and datetime.now(timezone.utc) >= submission.scheduled_at:
                    await blast(bot, submission.id, submission.gg_voice_final)

        except Exception as e:
            print(f"[Blast Scheduler] Error: {e}")

        await asyncio.sleep(BLAST_INTERVAL_SECONDS)

async def blast(bot: Bot, submission_id: int, message_text: str):
    characters = gossip_girl.list_characters()

    for character in characters:
        try:
            await bot.send_message(chat_id=character.telegram_id, text=message_text, parse_mode="HTML")
        except Exception as e:
            print(f"Failed to send blast to {character.telegram_id}: {e}")

    await gossip_girl.blast(submission_id)