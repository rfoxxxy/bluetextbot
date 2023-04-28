import html
import inspect
from typing import Callable

from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import (CallbackQuery, ChosenInlineResult, InlineQuery,
                           Message)
from loguru import logger

from bot_template import db, dp
from bot_template.database import database
from bot_template.database.exceptions import NotFoundError


class UserInjectorMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        handler: Callable = current_handler.get()
        has_user_arg = any(x == "user" for x in inspect.signature(handler).parameters)
        if not has_user_arg:
            user = None
        else:
            if "session" in data:
                try:
                    user = await database.get_user(message.from_user.id, data['session'])
                    if user.username != message.from_user.username:
                        user.username = message.from_user.username  # type: ignore
                    if user.name != html.escape(message.from_user.full_name):
                        user.name = html.escape(message.from_user.full_name)  # type: ignore
                    await data['session'].commit()
                except NotFoundError:
                    user = await database.register_user(message, data['session'])
            else:
                async with db.Session() as session:  # type: ignore
                    try:
                        user = await database.get_user(message.from_user.id, session)
                        if user.username != message.from_user.username:
                            user.username = message.from_user.username  # type: ignore
                        if user.name != html.escape(message.from_user.full_name):
                            user.name = html.escape(message.from_user.full_name)  # type: ignore
                        await session.commit()
                    except NotFoundError:
                        user = await database.register_user(message, session)
        data['user'] = user
        logger.debug(data['user'])

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        handler: Callable = current_handler.get()
        has_user_arg = any(x == "user" for x in inspect.signature(handler).parameters)
        if not has_user_arg:
            user = None
        else:
            if "session" in data:
                try:
                    user = await database.get_user(call.from_user.id, data['session'])
                    if user.username != call.from_user.username:
                        user.username = call.from_user.username  # type: ignore
                    if user.name != html.escape(call.from_user.full_name):
                        user.name = html.escape(call.from_user.full_name)  # type: ignore
                    await data['session'].commit()
                except NotFoundError:
                    user = await database.register_user(call, data['session'])
            else:
                async with db.Session() as session:  # type: ignore
                    try:
                        user = await database.get_user(call.from_user.id, session)
                        if user.username != call.from_user.username:
                            user.username = call.from_user.username  # type: ignore
                        if user.name != html.escape(call.from_user.full_name):
                            user.name = html.escape(call.from_user.full_name)  # type: ignore
                        await session.commit()
                    except NotFoundError:
                        user = await database.register_user(call, session)
        data['user'] = user
        logger.debug(data['user'])

    async def on_process_inline_query(self, query: InlineQuery, data: dict):
        handler: Callable = current_handler.get()
        has_user_arg = any(x == "user" for x in inspect.signature(handler).parameters)
        if not has_user_arg:
            user = None
        else:
            if "session" in data:
                try:
                    user = await database.get_user(query.from_user.id, data['session'])
                    if user.username != query.from_user.username:
                        user.username = query.from_user.username  # type: ignore
                    if user.name != html.escape(query.from_user.full_name):
                        user.name = html.escape(query.from_user.full_name)  # type: ignore
                    await data['session'].commit()
                except NotFoundError:
                    user = await database.register_user(query, data['session'])
            else:
                async with db.Session() as session:  # type: ignore
                    try:
                        user = await database.get_user(query.from_user.id, session)
                        if user.username != query.from_user.username:
                            user.username = query.from_user.username  # type: ignore
                        if user.name != html.escape(query.from_user.full_name):
                            user.name = html.escape(query.from_user.full_name)  # type: ignore
                        await session.commit()
                    except NotFoundError:
                        user = await database.register_user(query, session)
        data['user'] = user
        logger.debug(data['user'])

    async def on_process_chosen_inline_result(self, chosen: ChosenInlineResult, data: dict):
        handler: Callable = current_handler.get()
        has_user_arg = any(x == "user" for x in inspect.signature(handler).parameters)
        if not has_user_arg:
            user = None
        else:
            if "session" in data:
                try:
                    user = await database.get_user(chosen.from_user.id, data['session'])
                    if user.username != chosen.from_user.username:
                        user.username = chosen.from_user.username  # type: ignore
                    if user.name != html.escape(chosen.from_user.full_name):
                        user.name = html.escape(chosen.from_user.full_name)  # type: ignore
                    await data['session'].commit()
                except NotFoundError:
                    user = await database.register_user(chosen, data['session'])
            else:
                async with db.Session() as session:  # type: ignore
                    try:
                        user = await database.get_user(chosen.from_user.id, session)
                        if user.username != chosen.from_user.username:
                            user.username = chosen.from_user.username  # type: ignore
                        if user.name != html.escape(chosen.from_user.full_name):
                            user.name = html.escape(chosen.from_user.full_name)  # type: ignore
                        await session.commit()
                    except NotFoundError:
                        user = await database.register_user(chosen, session)
        data['user'] = user
        logger.debug(data['user'])


dp.middleware.setup(UserInjectorMiddleware())
