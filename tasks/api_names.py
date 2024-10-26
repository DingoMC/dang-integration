from models.mcuser import MCUser
from utils.mcapi import GetNameByUUID
from utils.console import ThreadInitialized, ThreadRunning, ThreadDone
import asyncio

VERSION = '0.1.1'
CONNECTOR = 'API->DB'
NAME = 'dang$$.mcnames.update'
INTERVAL = 86400
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def updater():
    data = MCUser.select(['uuid', 'mcuuid'])
    for user in data:
        name = GetNameByUUID(user[1])
        if len(name) > 0:
            MCUser.updateRow({"name": name}, {"uuid": user[0]})

async def interval():
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Updating Minecraft Names'))
        updater()
        print(ThreadDone(CONNECTOR, NAME))
        await asyncio.sleep(INTERVAL)

def main():
    print(ThreadInitialized(CONNECTOR, NAME, VERSION))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(interval())
