import sys
from asyncio import sleep

import pytest

sys.path.append('./')

from bot_template.utils import run_async  # pylint: disable=import-error


@pytest.mark.asyncio
async def test_asynctools():
    """If uvloop and nest_asyncio disabled - RuntimeError will be raised.
    Because this behavior isn't intended in project - we test that no RuntimeError is raised in normal mode
    """
    async def coro2():
        await sleep(3)
        return 2 + 2

    async def coro1():
        run_async(coro2)
        return 2 + 2

    run_async(coro1)
