from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ChatType
from api.gpt import gg_snark

router = Router()

@router.message(lambda m: m.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP))
async def snarky_reply(message: Message):
    if (
        message.reply_to_message and
        message.reply_to_message.from_user.is_bot and
        not message.from_user.is_bot
    ):
        gg_message = message.reply_to_message.text
        user_message = message.text

        snark = await gg_snark(gg_message=gg_message, user_reply=user_message)

        if snark:
            await message.reply(clean_snark(snark), parse_mode="HTML")

def clean_snark(text: str) -> str:
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1].strip()
    return text