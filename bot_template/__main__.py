from loguru import logger

from bot_template import (PROJECT_NAME, config, dp, features, is_custom_server,
                          is_prod, loop, scheduler)
from bot_template.core import BotCore

logger.info(
    f"Using features: {', '.join([x.split('_', maxsplit=1)[1] for x, _ in features if x.startswith('use')])}"
)
if is_prod:
    logger.warning("Running in production!")
if is_custom_server:
    logger.warning(
        f"Using custom BotAPI server: {config.get_item('features.custom_server', 'server')}"
    )

core = BotCore(PROJECT_NAME, is_prod, dp, loop, config, scheduler)

core.start()
