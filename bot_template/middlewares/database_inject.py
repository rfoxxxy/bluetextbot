import inspect
from typing import Callable

from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import (CallbackQuery, ChosenInlineResult, InlineQuery,
                           Message)
from loguru import logger

from bot_template import db, dp


class DatabaseInjectorMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        handler: Callable = current_handler.get()
        has_session_arg = any(x == "session" for x in inspect.signature(handler).parameters)
        if not has_session_arg:
            session = None
        else:
            session = db.Session()  # type: ignore
        data['session'] = session

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        handler: Callable = current_handler.get()
        has_session_arg = any(x == "session" for x in inspect.signature(handler).parameters)
        if not has_session_arg:
            session = None
        else:
            session = db.Session()  # type: ignore
        data['session'] = session

    async def on_process_inline_query(self, query: InlineQuery, data: dict):
        handler: Callable = current_handler.get()
        has_session_arg = any(x == "session" for x in inspect.signature(handler).parameters)
        if not has_session_arg:
            session = None
        else:
            session = db.Session()  # type: ignore
        data['session'] = session

    async def on_process_chosen_inline_result(self, chosen: ChosenInlineResult, data: dict):
        handler: Callable = current_handler.get()
        has_session_arg = any(x == "session" for x in inspect.signature(handler).parameters)
        if not has_session_arg:
            session = None
        else:
            session = db.Session()  # type: ignore
        data['session'] = session

    async def on_post_process_message(self, event: dict, message: Message, data: dict):
        logger.debug(data)
        if data.get('session'):
            await data['session'].close()

    async def on_post_process_callback_query(self, event: dict, call: CallbackQuery, data: dict):
        logger.debug(data)
        if data.get('session'):
            await data['session'].close()

    async def on_post_process_inline_query(self, event: dict, query: InlineQuery, data: dict):
        logger.debug(data)
        if data.get('session'):
            await data['session'].close()

    async def on_post_process_chosen_inline_result(self, event: dict, chosen: ChosenInlineResult, data: dict):
        logger.debug(data)
        if data.get('session'):
            await data['session'].close()


dp.middleware.setup(DatabaseInjectorMiddleware())
