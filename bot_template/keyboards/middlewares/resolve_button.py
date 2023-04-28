import pickle
from base64 import b64decode

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery

from bot_template.keyboards.database import database


class CallbackButtonMiddleware(BaseMiddleware):
    async def on_pre_process_callback_query(self, call: CallbackQuery,
                                            data: dict):
        raw_callback_data = call.data
        resolved_data = await database.get_callback(raw_callback_data)
        if not resolved_data:
            data['callback_object'] = {}
            data['callback_data'] = {}
        elif resolved_data == "died":
            await call.answer("Кнопка более неактивна. Повторите запрос.",
                              True)
            raise CancelHandler
        else:
            call.data = resolved_data.original_query
            data['callback_object'] = resolved_data.to_dict()
            data['callback_data'] = pickle.loads(
                b64decode(resolved_data.data.encode()))
