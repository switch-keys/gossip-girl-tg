from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import start, gossip
import asyncio
import os

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        gossip.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())