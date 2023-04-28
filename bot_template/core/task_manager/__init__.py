from asyncio import AbstractEventLoop, Task
from typing import List, Set

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from bot_template.core.config_manager.types.exceptions.feature_unavailable import \
    FeatureUnavailableError
from bot_template.core.task_manager.core import BaseCoreTask
from bot_template.core.task_manager.scheduler import BaseSchedulerTask


class TaskManager:  # TODO: make TaskManager a base class by analogy with ConfigManager and similar
    __slots__ = [
        "scheduler", "loop", "__pending_core_tasks",
        "__pending_scheduler_tasks", "__running_core_tasks"
    ]

    def __init__(self,
                 loop: AbstractEventLoop,
                 scheduler: AsyncIOScheduler | None = None) -> None:
        self.scheduler = scheduler
        self.loop = loop
        self.__pending_core_tasks: List[BaseCoreTask] = []
        self.__pending_scheduler_tasks: List[BaseSchedulerTask] = []
        self.__running_core_tasks: Set[Task] = set()

    def add_core_task(self, task: BaseCoreTask):
        """Add core task to run. Core tasks running once on startup

        Args:
            task (BaseCoreTask): Task object
        """
        self.__pending_core_tasks.append(task)

    def add_core_tasks(self, *args: BaseCoreTask):
        """Add multiple core tasks. Core tasks running once on startup
        """
        self.__pending_core_tasks.extend(args)

    def run_core_tasks(self):
        """Run core tasks
        """
        ready_tasks = [
            task for task in self.__pending_core_tasks
            if hasattr(task, "name")
        ]
        if not ready_tasks:
            return
        logger.info(
            f"Core tasks to be runned: {', '.join([task.name for task in ready_tasks])}"
        )
        for task in ready_tasks:
            logger.info(f"Running core task {task.name}...")
            _task = self.loop.create_task(task.run_task())
            self.__running_core_tasks.add(_task)
            _task.add_done_callback(self.__running_core_tasks.discard)

    def add_scheduler_task(self, task: BaseSchedulerTask):
        """Add scheduler task to run

        Args:
            task (BaseSchedulerTask): Task object
        """
        self.__pending_scheduler_tasks.append(task)

    def add_scheduler_tasks(self, *args: BaseSchedulerTask):
        """Add multiple scheduler tasks
        """
        self.__pending_scheduler_tasks.extend(args)

    def push_pending_scheduler_tasks(self):
        """Push pending scheduler tasks to scheduler

        Raises:
            FeatureUnavailableError: feature use_apscheduler required in order to call this method
        """
        if not self.scheduler:
            raise FeatureUnavailableError(
                "Feature use_apscheduler required in order to call this method"
            )
        ready_tasks = [
            task for task in self.__pending_scheduler_tasks
            if hasattr(task, "name") and hasattr(task, "trigger")
            and hasattr("task", "force_reschedule")
        ]
        if not ready_tasks:
            return
        for task in ready_tasks:
            if task.force_reschedule:
                if self.scheduler.get_job(job_id=task.name):
                    self.scheduler.remove_job(job_id=task.name)
            self.scheduler.add_job(
                func=task.run_task,
                trigger=task.trigger,
                id=task.name,
                misfire_grace_time=1 if not hasattr(task, "misfire_grace_time")
                else task.misfire_grace_time)
            self.__pending_scheduler_tasks.remove(task)

    def cancel_scheduler_task(self, task_name: str) -> bool:
        """Cancel scheduler task

        Args:
            task_name (str): task name

        Raises:
            FeatureUnavailableError: feature use_apscheduler required in order to call this method

        Returns:
            bool: success
        """
        if not self.scheduler:
            raise FeatureUnavailableError(
                "Feature use_apscheduler required in order to call this method"
            )
        if self.scheduler.get_job(job_id=task_name):
            self.scheduler.remove_job(job_id=task_name)
        return True


__all__ = ("BaseCoreTask", "BaseSchedulerTask")
