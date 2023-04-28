import html

import babel.numbers
import validators
from aiogram import types
from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo
from babel import Locale

from bot_template.keyboards.exceptions import UnsupportedTypeError
from bot_template.keyboards.models.base import BaseKeyboardButton
from bot_template.keyboards.utils import get_pay_text


class WebAppButton(BaseKeyboardButton):
    """Bottom and inline keyboard button object
    """
    def __init__(self, text: str, webapp_url: str):
        super().__init__("webapp", text, url=webapp_url)

    async def build_button(self, ctx):
        match type(ctx).__name__:
            case "InlineKeyboard":
                return InlineKeyboardButton(self.text, web_app=WebAppInfo(url=self.url))
            case "BottomKeyboard":
                return KeyboardButton(self.text, web_app=WebAppInfo(url=self.url))
            case _:
                raise UnsupportedTypeError(f"Type {self.type} isn't supported in {type(ctx).__name__}")


class PayWebAppButton(BaseKeyboardButton):
    """Bottom and inline keyboard button object
    """
    def __init__(self,
                 price: float,
                 val: str,
                 webapp_url: str,
                 locale: str | Locale = None):
        if not locale:
            locale = types.User.get_current().locale
        super().__init__(
            "webapp",
            f"{get_pay_text(str(locale))} {babel.numbers.format_currency(price, val, locale=locale)}",
            url=webapp_url)

    async def build_button(self, ctx):
        match type(ctx).__name__:
            case "InlineKeyboard":
                return InlineKeyboardButton(self.text, web_app=WebAppInfo(url=self.url))
            case "BottomKeyboard":
                return KeyboardButton(self.text, web_app=WebAppInfo(url=self.url))
            case _:
                raise UnsupportedTypeError(f"Type {self.type} isn't supported in {type(ctx).__name__}")


class MarkdownViewWebAppButton(BaseKeyboardButton):
    """Bottom and inline keyboard button object
    """
    def __init__(self, text: str, md_url: str):
        _md_url = f"https://static.neonteam.cc/{md_url}" \
            if not validators.url(md_url, public=True) else md_url
        super().__init__(
            "webapp",
            text,
            url=
            f"https://static.neonteam.cc/tgmd.html?url={html.escape(_md_url)}")

    async def build_button(self, ctx):
        match type(ctx).__name__:
            case "InlineKeyboard":
                return InlineKeyboardButton(self.text, web_app=WebAppInfo(url=self.url))
            case "BottomKeyboard":
                return KeyboardButton(self.text, web_app=WebAppInfo(url=self.url))
            case _:
                raise UnsupportedTypeError(f"Type {self.type} isn't supported in {type(ctx).__name__}")
