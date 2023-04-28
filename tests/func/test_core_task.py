import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

LOGGER = logging.getLogger(__name__)

sys.path.append('./')

from bot_template.core import BotCore  # pylint: disable=import-error
from bot_template.core.task_manager import \
    BaseCoreTask  # pylint: disable=import-error


def test_core_tasks(config_manager, event_loop):
    class TestTask(BaseCoreTask):
        name = "test task"

        async def run_task(self):
            LOGGER.info("tesk task executed!")

    async def polling_mock():
        await asyncio.sleep(3)

    core = BotCore("bot_template", False, Dispatcher(Bot("42:TEST")),
                   event_loop, config_manager)
    task = TestTask()
    core.add_core_task(task)
    core.add_core_tasks(*[task for _ in range(4)])

    assert len(core.task_manager._TaskManager__pending_core_tasks) == 5  # pylint: disable=protected-access
    core._BotCore__run_core_tasks()  # pylint: disable=protected-access

    event_loop.run_until_complete(polling_mock())
