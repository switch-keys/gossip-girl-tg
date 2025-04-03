import asyncio
from typing import List
from aiogram.types import Message

async def delete_with_delay(messages: List[Message], delay_seconds: int = 5):
    await asyncio.sleep(delay_seconds)

    for msg in messages:
        try:
            await msg.delete()
        except Exception as e:
            print(f"[Delete Error] Failed to delete message {msg.message_id}: {e}")