import asyncio
import logging
import os
import time
from argparse import ArgumentParser
from pathlib import Path

os.environ[
    "DISABLE_UVLOOP"] = "True"  # prevent aiogram from patching asyncio with uvloop

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from cachetools import TTLCache
from loguru import logger

from bot_template.core.config_manager import ConfigManager

arg_parser = ArgumentParser()
arg_parser.add_argument("--recreate",
                        action="store_true",
                        help="Recreate database")
args, _ = arg_parser.parse_known_args()

config = ConfigManager("config.toml", True)

features = list(
    filter(lambda feature: feature[1],
           config.get_section("features").items()))

# since nest_asyncio doesn't support uvloop and other custom event loop policies,
# there's a double-edged sword - allow nesting slow asyncio or use faster uvloop w/o nesting
if config.get_item("features", "use_uvloop"):
    from uvloop import EventLoopPolicy
    asyncio.set_event_loop_policy(EventLoopPolicy())
    del os.environ["DISABLE_UVLOOP"]
else:
    import nest_asyncio
    nest_asyncio.apply()

import sqlalchemy
from aiogram import Bot, Dispatcher
from aiogram.bot.api import TELEGRAM_PRODUCTION, TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine

is_prod = os.environ.get("ENV") == "production" or config.get_item(
    "telegram", "prod")
is_custom_server = config.get_item("features", "use_custom_server")
PROJECT_NAME = __name__
_startup_time = time.time()

admins = config.get_item("bot", "admins")
RECREATE_DB = args.recreate

cache = TTLCache(maxsize=float('inf'),
                 ttl=config.get_item("bot", "throttling"))
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
bot = Bot(
    config.get_item("telegram", "token") if is_prod else config.get_item(
        "telegram", "beta_token"),
    parse_mode="html",  # noqa: e126
    server=TelegramAPIServer.from_base(
        config.get_item('features.custom_server', 'server'))
    if is_custom_server else TELEGRAM_PRODUCTION)
dp = Dispatcher(
    bot,
    storage=RedisStorage2(config.get_item("features.redis", "addr"),
                          config.get_item("features.redis", "port"),
                          password=config.get_item("features.redis", "pass"),
                          prefix=config.get_item("features.redis", "prefix"))
    if config.get_item("features", "use_redis_fsm") else MemoryStorage())

scheduler = None  # pylint: disable=invalid-name

if config.get_item("features", "use_apscheduler"):
    logging.getLogger('apscheduler').setLevel(logging.INFO)
    scheduler = AsyncIOScheduler(loop=loop,
                                 timezone=config.get_item(
                                     "features.apscheduler", "timezone"))
    scheduler.add_jobstore('sqlalchemy', url="sqlite:///static/jobs.sqlite3")

bot['config'] = config


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # type: ignore
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth,
                   exception=record.exc_info).log(level, record.getMessage())


if config.get_item("features", "use_file_logs"):
    logger.add("static/logs/debug.log",
               rotation="10MB",
               compression="zip",
               backtrace=True,
               diagnose=True,
               enqueue=True,
               level="DEBUG")
    logger.add("static/logs/base.log",
               rotation="10MB",
               compression="zip",
               enqueue=True,
               level="INFO")
    logger.add("static/logs/error.log",
               rotation="10MB",
               compression="zip",
               backtrace=True,
               diagnose=True,
               enqueue=True,
               level="ERROR")

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)

if config.get_item("features", "use_database"):
    from bot_template.database import \
        Database  # pylint: disable=ungrouped-imports
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.INFO)
    engine = create_async_engine(sqlalchemy.engine.URL.create(
        drivername=config.get_item("features.database", "driver"),
        username=config.get_item("features.database", "username"),
        password=config.get_item("features.database", "password"),
        host=config.get_item("features.database", "addr"),
        port=config.get_item("features.database", "port"),
        database=config.get_item("features.database", "database_name")),
                                 future=True)  # noqa: e126
    db = Database(engine, RECREATE_DB)
