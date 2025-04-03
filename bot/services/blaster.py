import asyncio
from aiogram import Bot
from datetime import datetime, timezone
from api import gossip_girl
import os

BLAST_INTERVAL_SECONDS = 60  # check every minute

async def loop(bot: Bot):
    while True:
        try:
            scheduled = await gossip_girl.list_scheduled()

            for submission in scheduled:
                if submission.scheduled_at and datetime.now(timezone.utc) >= submission.scheduled_at.replace(tzinfo=timezone.utc):
                    await blast(bot, submission.id, submission.gg_voice_final)

        except Exception as e:
            print(f"[Blast Scheduler] Error: {e}")

        await asyncio.sleep(BLAST_INTERVAL_SECONDS)

async def blast(bot: Bot, submission_id: int, message_text: str):
    try:
        group_chat_id = int(os.getenv("GROUP_CHAT_ID"))
        sent_message = await bot.send_message(
            chat_id=group_chat_id , 
            text=message_text, 
            parse_mode="HTML")
        await bot.pin_chat_message(
            chat_id=group_chat_id , 
            message_id=sent_message.message_id,
            disable_notification=True)
        await gossip_girl.blast(submission_id)
    except Exception as e:
        print(f"Failed to send blast: {e}")