from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from bot.handlers import start, gossip, review, nickname, assign_gg, reset, snark, bypass, schedule, group_joins, characters
from bot.callbacks import common, review as review_callback, nickname as nickname_callback, assign_gg as assign_gg_callback
from bot.services import blaster
from db.database import init_db
import asyncio
import os

async def main():
    await init_db()
    bot = Bot(
        token=os.getenv("BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        reset.router,
        review.router,
        nickname.router,
        review_callback.router,
        nickname_callback.router,
        assign_gg.router,
        assign_gg_callback.router,
        group_joins.router,
        characters.router,
        snark.router,
        common.router,
        bypass.router,
        schedule.router,
        gossip.router
    )

    asyncio.create_task(blaster.loop(bot))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())