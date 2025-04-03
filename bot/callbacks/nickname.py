from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.states.nickname import Nickname
from aiogram.types import ForceReply

router = Router()

@router.callback_query(F.data.startswith("nickname:set:"))
async def handle_user_selected(callback: types.CallbackQuery, state: FSMContext):
    print("✅ Nickname (set) callback fired")
    telegram_id = int(callback.data.split(":")[2])
    await state.update_data(target_telegram_id=telegram_id)
    await state.set_state(Nickname.waiting_for_input)
    await callback.message.answer("What’s the new nickname, darling?", reply_markup=ForceReply())
    await callback.message.delete()
