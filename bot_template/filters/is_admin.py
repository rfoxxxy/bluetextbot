from typing import Union

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery, Message

from bot_template import admins, dp


class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, event: Union[Message, CallbackQuery]) -> bool:
        return event.from_user.id in admins and self.is_admin


dp.filters_factory.bind(
    AdminFilter,
    event_handlers=[dp.message_handlers, dp.callback_query_handlers])
