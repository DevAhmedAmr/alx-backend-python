#!/usr/bin/env python3
import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    execute async_comprehension four times in parallel using asyncio.gather.

    measure_runtime  measures the total runtime and return it.

        Returns:
                float : total runtime
    """
    start_time = time.time()

    list1, list2, list3, lst4 = await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension())

    return time.time() - start_time
