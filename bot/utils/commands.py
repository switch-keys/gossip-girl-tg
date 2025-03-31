from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

async def set_role_commands(bot: Bot, telegram_id: int, role: str):
    base = [BotCommand(command="start", description="Join the game")]

    if role in ("GOSSIP_GIRL", "ADMIN"):
        base.extend([
            BotCommand(command="nickname", description="Change a user's nickname"),
            BotCommand(command="review", description="Review and manage gossip submissions"),
        ])

    if role == "ADMIN":
        base.append(BotCommand(command="assign_gg", description="Appoint Gossip Girl"))

    await bot.set_my_commands(
        commands=base,
        scope=BotCommandScopeChat(chat_id=telegram_id)
    )
