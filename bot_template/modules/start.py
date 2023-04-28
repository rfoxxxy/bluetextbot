from aiogram import types

from bot_template import dp
from bot_template.keyboards.models import (ButtonRow, CallbackButton,
                                           InlineKeyboard,
                                           MarkdownViewWebAppButton,
                                           URLPayButton, WebAppButton)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    return await message.reply("hello, world!")


@dp.message_handler(commands=['test'])
async def test_handler(message: types.Message):
    keyboard = InlineKeyboard(
        ButtonRow(
            MarkdownViewWebAppButton(
                "Read me",
                "https://raw.githubusercontent.com/rfoxxxy/telegram-bot-template/main/README.md"
            )),
        ButtonRow(CallbackButton("test callback", "test_callback"),
                  WebAppButton("test webapp", "https://google.com")),
        ButtonRow(URLPayButton(10000, "USD", "https://google.com")))
    return await message.reply("test!", reply_markup=keyboard)
