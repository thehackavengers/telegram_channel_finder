import asyncio
import random


async def random_delay():

    wait = random.uniform(2,5)

    await asyncio.sleep(wait)