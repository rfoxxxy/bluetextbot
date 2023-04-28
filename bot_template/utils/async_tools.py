import asyncio
import functools
import threading
import typing
from typing import Awaitable, Callable

from bot_template import config


class _RunAsyncInThread(threading.Thread):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        super().__init__()

    def run(self):
        self.result = asyncio.run(self.func(*self.args, **self.kwargs))


def run_sync(func: Callable, *args, **kwargs) -> Awaitable:
    """Run sync function in async context

    Args:
        func (Callable): function to be runned

    Returns:
        Awaitable: coroutine that can be awaited
    """
    return asyncio.get_running_loop() \
        .run_in_executor(None,
                         functools.partial(func,
                                           *args,
                                           **kwargs))


def run_async(func: Awaitable,
              *args,
              prevent_using_loop: bool = False,
              **kwargs) -> typing.Any:
    """Run async function as sync and block till end

    Args:
        func (Awaitable): coroutine that needs to be runned
        prevent_using_loop (bool): prevent from using free and not running loop

    Returns:
        typing.Any: result
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if (loop and loop.is_running() and config.get_item(
            "features", "use_uvloop")) or prevent_using_loop:
        thread = _RunAsyncInThread(func, args, kwargs)
        thread.start()
        thread.join()
        return thread.result
    return asyncio.run(func(*args, **kwargs))
