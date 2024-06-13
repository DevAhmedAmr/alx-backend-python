#!/usr/bin/env python3
import asyncio
import time
"""module doc """

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    execute async_comprehension four times in parallel using asyncio.gather.

    measure_runtime  measures the total runtime and return it.

        Returns:
                float : total runtime
    """
    start_time = time.perf_counter()
    # await asyncio.gather(async_comprehension(), async_comprehension(),
    #                      async_comprehension(), async_comprehension())
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension())

    return time.perf_counter() - start_time
