import random
import time


async def async_generator():
    for i in range(10):
        time.sleep(1)
        yield random.uniform(0, 10)


if "__main__" == __name__:
    import asyncio

    async def print_yielded_values():
        result = []
        async for i in async_generator():
            result.append(i)
        print(result)

asyncio.run(print_yielded_values())
