#!/usr/bin/env python3
import asyncio
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension():
    """
        collect 10 random numbers using an async comprehension
        over async_generator, then return the 10 random numbers.

    """
    return [num async for num in async_generator()]


async def main():
    print(await async_comprehension())

asyncio.run(main())
