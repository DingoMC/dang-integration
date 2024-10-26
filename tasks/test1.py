import time
import asyncio

async def async_test1():
    for i in range(5):
        print(f"Thread-1 - {i}")
        await asyncio.sleep(1)
    
def test1():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_test1())

async def async_test2():
    for i in range(5):
        print(f"Thread-2 - {i}")
        await asyncio.sleep(1)

def test2():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_test2())