from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import start, gossip, review, nickname, assign_gg
from bot.callbacks import review as review_callback, nickname as nickname_callback, assign_gg as assign_gg_callback
from bot.services import blaster
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        gossip.router,
        review.router,
        nickname.router,
        review_callback.router,
        nickname_callback.router,
        assign_gg.router,
        assign_gg_callback.router
    )

    asyncio.create_task(blaster.loop(bot))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())