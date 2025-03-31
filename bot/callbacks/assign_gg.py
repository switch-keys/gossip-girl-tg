from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from api import admin
from bot.utils import keyboards
from bot.states.assign_gg import AssignGG
from bot.utils.commands import set_role_commands

router = Router()

@router.callback_query(F.data.startswith("assign_gg:select:"))
async def handle_user_selection(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = int(callback.data.split(":")[2])
    display_name = int(callback.data.split(":")[3])

    await state.update_data(target_telegram_id=telegram_id)
    await state.set_state(AssignGG.waiting_for_confirmation)

    await callback.message.edit_text(
        f"Are you sure you want to make <b>{display_name}</b> Gossip Girl?",
        reply_markup=keyboards.assign_gg_confirm(telegram_id),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "assign_gg:cancel")
async def handle_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Gossip Girl remains a mystery... for now. ❌")

@router.callback_query(F.data.startswith("assign_gg:confirm:"))
async def handle_confirm(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = int(callback.data.split(":")[2])
    old_gg, new_gg = await admin.assign_gg(telegram_id)
    await set_role_commands(callback.bot, old_gg.telegram_id, old_gg.role)
    await set_role_commands(callback.bot, new_gg.telegram_id, new_gg.role)
    await state.clear()
    await callback.message.edit_text("The deed is done. Gossip Girl has been chosen. XOXO 💋")
