from models.playtime import Playtime
from models.mcuser import MCUser
from utils.mccon import GetScore, NO_SCORE
from utils.console import ThreadInitialized, ThreadRunning, ThreadDone
import asyncio

VERSION = '0.1.2'
CONNECTOR = 'MC->DB'
NAME = 'dang$$.playtime.update'
INTERVAL = 1800
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def updater():
    data = MCUser.select(['uuid', 'mcuuid', 'name'])
    for user in data:
        hours = GetScore('/root/minecraft_m/minigames/data/scoreboard.dat',user[2],'Hours')
        if hours > NO_SCORE:
            Playtime.updateRow({"hours": hours}, {"uuid": user[0], "server_id": 3})

async def interval():
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Updating playtimes'))
        updater()
        print(ThreadDone(CONNECTOR, NAME))
        await asyncio.sleep(INTERVAL)

def main():
    print(ThreadInitialized(CONNECTOR, NAME, VERSION))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(interval())
