from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from bot_template import cache, dp


class ThrottlingMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        if message.is_command():
            if not cache.get(message.from_user.id):
                cache[message.from_user.id] = True
                return
            await message.reply("Тише-тише! Попробуй снова через 1 сек.")
            raise CancelHandler

    async def on_pre_process_callback_query(self, call: CallbackQuery, data: dict):
        if not cache.get(call.from_user.id):
            cache[call.from_user.id] = True
            return
        await call.answer("Тише-тише! Попробуй снова через 1 сек.", True)
        raise CancelHandler


dp.middleware.setup(ThrottlingMiddleware())
