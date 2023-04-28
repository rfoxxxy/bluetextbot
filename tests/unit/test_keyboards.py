import logging
import sys

LOGGER = logging.getLogger(__name__)

sys.path.append('./')

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from bot_template import keyboards  # pylint: disable=import-error


class TestKeyboards:
    def test_inline_own_keyboard_equals_aiogram_keyboard(self):
        own_keyboard = keyboards.InlineKeyboard(
            keyboards.ButtonRow(
                keyboards.CallbackButton("test", "test"),
                keyboards.URLButton("google", "https://google.com")),
            keyboards.ButtonRow(keyboards.CallbackButton("test 2", "test2")))

        aiogram_keyboard = InlineKeyboardMarkup().row(
            InlineKeyboardButton("test", callback_data="test"),
            InlineKeyboardButton("google", url="https://google.com")).row(
                InlineKeyboardButton("test 2", callback_data="test2"))

        assert aiogram_keyboard.to_python() == own_keyboard.to_python()

    def test_reply_own_keyboard_equals_aiogram_keyboard(self):
        own_keyboard = keyboards.BottomKeyboard(
            keyboards.ButtonRow(keyboards.TextButton("test")),
            keyboards.ButtonRow(keyboards.TextButton("test 2")))

        aiogram_keyboard = ReplyKeyboardMarkup(
            one_time_keyboard=False, resize_keyboard=True,
            selective=False).row(KeyboardButton("test")).row(
                KeyboardButton("test 2"))

        assert aiogram_keyboard.to_python() == own_keyboard.to_python()
