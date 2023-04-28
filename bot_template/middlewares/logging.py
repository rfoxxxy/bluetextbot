from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import (CallbackQuery, ChosenInlineResult, InlineQuery,
                           Message)

from bot_template import config, dp, logger
from bot_template.keyboards.utils import get_button_text


class LogMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        logger.info(f"MESSAGE | user_id: {message.from_user.id} (name: {message.from_user.full_name} "
                    f"| username: {message.from_user.username} | locale: {message.from_user.locale}"
                    f"{f' | chat: {message.chat.title} ({message.chat.username or message.chat.id})' if message.chat.id != message.from_user.id else ''}) | "
                    f"text: {message.text or message.caption}")

    async def on_pre_process_callback_query(self, call: CallbackQuery, data: dict):
        raw_data = data.get('callback_object', {}).get('query', call.data)
        button_text = get_button_text(call, raw_data)
        logger.info(f"CALLBACK | user_id: {call.from_user.id} (name: {call.from_user.full_name} "
                    f"| username: {call.from_user.username} | locale: {call.from_user.locale}"
                    f"{f' | chat: {call.message.chat.title} ({call.message.chat.username or call.message.chat.id})' if call.message.chat.id != call.from_user.id else ''}) | "
                    f"{f'raw_data: {raw_data} | ' if config.get_item('features', 'use_modern_callback') else ''}"
                    f"data: {call.data} | button_text: {button_text}")

    async def on_pre_process_inline_query(self, query: InlineQuery, data: dict):
        logger.info(f"INLINE | user_id: {query.from_user.id} (name: {query.from_user.full_name}"
                    f"| username: {query.from_user.username} | "
                    f"locale: {query.from_user.locale}) | data: {query.query}")

    async def on_pre_process_chosen_inline_result(self, chosen: ChosenInlineResult, data: dict):
        logger.info(f"CHOSEN INLINE | user_id: {chosen.from_user.id} (name: {chosen.from_user.full_name} | "
                    f"username: {chosen.from_user.username} | locale: {chosen.from_user.locale}) "
                    f"| data: {chosen.query} | chosen: {chosen.result_id} (inline_message_id: {chosen.inline_message_id})")


dp.middleware.setup(LogMiddleware())
