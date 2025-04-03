from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from db.model import Character

def review(submission_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Reject 🚫", callback_data=f"review:skip:{submission_id}"),
            InlineKeyboardButton(text="Schedule ⏰", callback_data=f"review:schedule:{submission_id}"),
            InlineKeyboardButton(text="Edit Message ✏️", callback_data=f"review:edit:{submission_id}"),
        ],
        [InlineKeyboardButton(text="❗ Abort", callback_data="common:abort")]
    ])

def edit_message(submission_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Accept ✅", callback_data=f"review2:accept_edit:{submission_id}"),
            InlineKeyboardButton(text="Undo Edit ↩️", callback_data=f"review2:undo_edit:{submission_id}")
        ],
        [InlineKeyboardButton(text="❗ Abort", callback_data="common:abort")]
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
        ],
        [InlineKeyboardButton(text="❗ Abort", callback_data="common:abort")]
    ])

def abort_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚫 Abort", callback_data="common:abort")]
        ]
    )

def exit():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚫 Exit", callback_data="common:abort")]
        ]
    )

def pronouns():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="He/Him", callback_data="pronouns:HE")],
            [InlineKeyboardButton(text="She/Her", callback_data="pronouns:SHE")],
            [InlineKeyboardButton(text="They/Them", callback_data="pronouns:THEY")]
        ]
    )