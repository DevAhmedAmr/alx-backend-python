#!/usr/bin/env python3
import random
import asyncio
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
	"""he coroutine will loop 10 times,
	each time asynchronously wait 1 second,
    then yield a random number between 0 and 10

	Yields:
		Generator[float, None, None]: _description_"""
    for i in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)


# if "__main__" == __name__:
#     import asyncio

#     async def print_yielded_values():
#         result = []
#         async for i in async_generator():
#             result.append(i)
#         print(result)

# asyncio.run(print_yielded_values())
