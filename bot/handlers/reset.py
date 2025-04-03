from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.utils.role_filter import RequireRole
from db.model import Role
from bot.utils.private_only import PrivateOnly
import asyncio
from bot.utils.delete_message import delete_with_delay

router = Router()
@router.message(Command("reset"), RequireRole([Role.ADMIN, Role.GOSSIP_GIRL]), PrivateOnly())
async def reset_handler(message: Message, state: FSMContext):
    print("✅ Reset handler fired")
    await state.clear()
    response = await message.answer("FSM cleared.")
    asyncio.create_task(delete_with_delay([response, message],3))
    
@router.message(Command("get_chat_id"))
async def get_chat_id(message: Message):
    await message.answer(f"Chat ID: <code>{message.chat.id}</code>", parse_mode="HTML")