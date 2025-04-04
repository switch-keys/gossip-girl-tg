from aiogram import Router, F
from aiogram.types import Message
router = Router()

@router.message(F.new_chat_members)
async def handle_new_member_join(message: Message, bot):
    for user in message.new_chat_members:
        # Post snarky message to group
        try:
            await message.answer(welcome_snark(user.first_name))
        except Exception as e:
            print(f"❌ Failed to snark in group: {e}")


def welcome_snark(first_name: str) -> str:
    return f"🧐 Look who just joined... \n <a href='https://t.me/gossipgirlgame_bot'>{first_name}, DM me to get started, sweetheart.</a>"