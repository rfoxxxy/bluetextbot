from aiogram import types

from bot_template.keyboards.utils.mixins import KeyboardMarkupMixin
from bot_template.keyboards.utils.payment import get_pay_text

__all__ = ("KeyboardMarkupMixin", "get_pay_text", "get_button_text")


def get_button_text(call: types.CallbackQuery, callback_data: str) -> str:
    """Get text from callback button by it's data

    Args:
        call (types.CallbackQuery): Callback query object
        callback_data (str): Callback button's data

    Returns:
        str: Callback button's text
    """
    for row in call.message.reply_markup['inline_keyboard']:
        for column in row:
            if column['callback_data'] == callback_data:
                return column['text']
    return ""
