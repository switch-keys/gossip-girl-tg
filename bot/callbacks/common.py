from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(lambda c: c.data == "common:abort")
async def handle_abort(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    try:
        await callback.message.delete()
    except Exception as e:
        print(f"[Abort Error] Couldn't delete message: {e}")

    # Don't send anything back — total stealth
    await callback.answer()  # ✅ Prevents "loading..." spinner