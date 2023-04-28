from asyncio import AbstractEventLoop
from typing import Awaitable

from aiogram import Dispatcher, executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from bot_template.core.config_manager import ConfigManager
from bot_template.core.loader import ModuleLoader
from bot_template.core.task_manager import (BaseCoreTask, BaseSchedulerTask,
                                            TaskManager)


class BotCore:
    __slots__ = [
        "project_name", "is_prod", "dp", "loop", "config", "webhook",
        "task_manager"
    ]

    def __init__(  # pylint: disable=too-many-arguments
            self,
            project_name: str,
            is_prod: bool,
            dp: Dispatcher,  # pylint: disable=invalid-name
            loop: AbstractEventLoop,
            config: ConfigManager,
            scheduler: AsyncIOScheduler | None = None) -> None:
        logger.info(f"Initializing {project_name}...")
        self.project_name = project_name
        self.is_prod = is_prod
        self.dp = dp  # pylint: disable=invalid-name
        self.loop = loop
        self.config = config
        self.webhook = config.get_item("features", "use_webhook")
        self.task_manager = TaskManager(self.loop, scheduler)

        if self.dp is not None:
            self.dp.bot["core"] = self

    def add_core_task(self, task: BaseCoreTask):
        """Add core task to run. Core tasks running once on startup

        Args:
            task (BaseCoreTask): Task object
        """
        self.task_manager.add_core_task(task)

    def add_core_tasks(self, *args: BaseCoreTask):
        """Add multiple core tasks. Core tasks running once on startup
        """
        self.task_manager.add_core_tasks(*args)

    def __run_core_tasks(self):
        """Run core tasks
        """
        return self.task_manager.run_core_tasks()

    def add_scheduler_task(self, task: BaseSchedulerTask):
        """Add scheduler task to run

        Args:
            task (BaseSchedulerTask): Task object
        """
        self.task_manager.add_scheduler_task(task)

    def add_scheduler_tasks(self, *args: BaseSchedulerTask):
        """Add multiple scheduler tasks
        """
        self.task_manager.add_scheduler_tasks(*args)

    def push_pending_scheduler_tasks(self):
        """Push pending scheduler tasks to scheduler

        Raises:
            FeatureUnavailableError: feature use_apscheduler required in order to call this method
        """
        return self.task_manager.push_pending_scheduler_tasks()

    def cancel_scheduler_task(self, task_name: str) -> bool:
        """Cancel scheduler task

        Args:
            task_name (str): task name

        Raises:
            FeatureUnavailableError: feature use_apscheduler required in order to call this method

        Returns:
            bool: success
        """
        return self.task_manager.cancel_scheduler_task(task_name)

    async def _startup(self, dispatcher: Dispatcher):
        """Main startup logic

        Args:
            dispatcher (Dispatcher): aiogram dispatcher object
        """
        if self.config.get_item("features", "use_modern_callback"):
            from bot_template.keyboards.middlewares import \
                CallbackButtonMiddleware  # pylint: disable=import-outside-toplevel
            dispatcher.middleware.setup(CallbackButtonMiddleware())

        ModuleLoader(self.project_name, self.is_prod, self.config).load_all()

        if self.config.get_item("features", "use_database"):
            from bot_template import \
                db  # pylint: disable=import-outside-toplevel
            await db.init_database()

        if self.task_manager and self.task_manager.scheduler:
            self.task_manager.scheduler.start()
            self.push_pending_scheduler_tasks()

        self.__run_core_tasks()

    async def _shutdown(self, dispatcher: Dispatcher):
        """Main shutdown logic

        Args:
            dispatcher (Dispatcher): aiogram dispatcher object
        """
        logger.warning("Closing Redis instance...")
        await dispatcher.storage.close()
        await dispatcher.storage.wait_closed()
        logger.info("Redis instance closed!")

    async def _startup_webhook(self, dispatcher: Dispatcher) -> Awaitable:
        """Startup logic for webhook

        Args:
            dispatcher (Dispatcher): aiogram dispatcher object

        Returns:
            Awaitable: main startup logic
        """

        skip_updates = self.config.get_item("telegram", "skip_updates")

        if skip_updates:
            await self.dp.bot.delete_webhook(True)

        webhook_url = f"{self.config.get_item('features.webhook', 'host')}{self.config.get_item('features.webhook', 'path')}"
        webhook_info = await self.dp.bot.get_webhook_info()
        if webhook_url != webhook_info.url or webhook_info.max_connections != 100:
            await self.dp.bot.set_webhook(webhook_url,
                                          max_connections=100,
                                          drop_pending_updates=skip_updates)
        return await self._startup(dispatcher)

    async def _startup_polling(self, dispatcher: Dispatcher) -> Awaitable:
        """Startup logic for polling

        Args:
            dispatcher (Dispatcher): aiogram dispatcher object

        Returns:
            Awaitable: main startup logic
        """

        webhook_info = await self.dp.bot.get_webhook_info()
        if webhook_info.url:
            await self.dp.bot.delete_webhook(
                self.config.get_item("telegram", "skip_updates"))
        return await self._startup(dispatcher)

    def start(self):
        """Start bot
        """
        logger.info(f"Starting {self.project_name}...")
        if self.webhook:
            executor.start_webhook(
                self.dp,
                webhook_path=self.config.get_item("features.webhook", "path"),
                host=self.config.get_item("features.webhook", "webapp_host"),
                port=self.config.get_item("features.webhook", "webapp_port"),
                loop=self.loop,
                on_startup=self._startup_webhook,
                on_shutdown=self._shutdown)
        else:
            executor.start_polling(self.dp,
                                   skip_updates=self.config.get_item(
                                       "telegram", "skip_updates"),
                                   loop=self.loop,
                                   on_startup=self._startup_polling,
                                   on_shutdown=self._shutdown)
