#!/usr/bin/env python3
import asyncio
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension():
    return list(async_generator())


async def main():
    print(await async_comprehension())

asyncio.run(main())
