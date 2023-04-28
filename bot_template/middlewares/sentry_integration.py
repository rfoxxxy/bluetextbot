import sentry_sdk
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from bot_template import config, dp


class SentryContextMiddleware(BaseMiddleware):
    @staticmethod
    async def on_pre_process_update(update: Update, data: dict):
        if (not update.message) and (not update.callback_query) and (not update.inline_query) and (not update.my_chat_member) and (not update.chosen_inline_result):
            return

        from_user = (update.message or update.callback_query or update.inline_query or update.my_chat_member or update.chosen_inline_result).from_user

        sentry_sdk.set_user({
            'name': from_user.full_name,
            'id': from_user.id,
            'username': from_user.username,
            'update': update.to_python()
        })


sentry_sdk.init(dsn=config.get_item("features.sentry", "public_key"),
                integrations=[AioHttpIntegration()],
                traces_sample_rate=config.get_item("features.sentry", "traces_sample_rate"))
dp.middleware.setup(SentryContextMiddleware())
