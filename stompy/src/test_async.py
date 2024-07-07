"""Async test functions."""

import time
import asyncio


async def fn1() -> int:
    await asyncio.sleep(5)
    return 1


async def fn2() -> int:
    await asyncio.sleep(5)
    return 2


def fn1_sync() -> int:
    time.sleep(5)
    return 1


def fn2_sync() -> int:
    time.sleep(5)
    return 2


async def main() -> None:
    # print(await asyncio.gather(fn1(), fn2()))
    print(fn1_sync(), fn2_sync())


if __name__ == "__main__":
    # python -m stompy.src.test_async
    asyncio.run(main())
