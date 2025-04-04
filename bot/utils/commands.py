from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from db.model import Role

async def set_role_commands(bot: Bot, telegram_id: int, role: str):
    base = [BotCommand(command="start", description="Join the game"),
            BotCommand(command="characters", description="Display the cast of Gossip Girl")]

    if role == Role.ADMIN:
        base.extend([
            BotCommand(command="nickname", description="Change a user's nickname"),
            BotCommand(command="review", description="Review and manage gossip submissions"),
            BotCommand(command="bypass", description="Admin gossip injection"),
            BotCommand(command="schedule", description="Display current blast schedule")
        ])
        
    await bot.set_my_commands(
        commands=base,
        scope=BotCommandScopeChat(chat_id=telegram_id)
    )
