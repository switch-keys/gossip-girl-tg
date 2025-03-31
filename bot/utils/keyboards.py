from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from db.model import Character

def review(submission_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Skip 🚫", callback_data=f"review:skip:{submission_id}"),
            InlineKeyboardButton(text="Schedule ⏰", callback_data=f"review:schedule:{submission_id}"),
            InlineKeyboardButton(text="Edit Message ✏️", callback_data=f"review:edit:{submission_id}"),
        ]
    ])

def edit_message(submission_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Accept ✅", callback_data=f"review:accept_edit:{submission_id}"),
            InlineKeyboardButton(text="Undo Edit ↩️", callback_data=f"review:undo_edit:{submission_id}")
        ]
    ])

def edit_nickname(characters: List[Character]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{character.display_name} ({character.nickname})",
                    callback_data=f"nickname:set:{character.telegram_id}"
                )
            ] for character in characters
        ]
    )

def assign_gg_select(characters: List[Character]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{character.display_name} ({character.nickname})",
                    callback_data=f"assign_gg:select:{character.telegram_id}:{character.display_name}"
                )
            ] for character in characters
        ]
    )

def assign_gg_confirm(telegram_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Yes ✅", callback_data=f"assign_gg:confirm:{telegram_id}"),
            InlineKeyboardButton(text="No ❌", callback_data="assign_gg:cancel")
        ]
    ])
