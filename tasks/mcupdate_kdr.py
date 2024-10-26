from models.mcuser import MCUser
from models.mcuser_kdr import MCUserKDR
from utils.mccon import GetScore, NO_SCORE
from utils.console import ThreadInitialized, ThreadRunning, ThreadDone
import asyncio

VERSION = '0.1.0'
CONNECTOR = 'MC->DB'
NAME = 'dang$$.kdr.update'
INTERVAL = 600
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def updater():
    data = MCUser.select(['uuid', 'name'])
    for user in data:
        kills = GetScore('/root/minecraft_m/minigames/data/scoreboard.dat',user[1],'Kills')
        deaths = GetScore('/root/minecraft_m/minigames/data/scoreboard.dat',user[1],'Deaths')
        if kills > NO_SCORE and deaths > NO_SCORE:
            kdr = 0.0
            if deaths > 0:
                kdr = float(kills) / float(deaths)
            MCUserKDR.upsert({"kills": kills, "deaths": deaths, "kdr": kdr, "updated_on": "NOW()"},
                user[0], 3, kills, deaths, kdr, {"uuid": user[0], "server_id": 3})

async def interval():
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Updating player KDRs'))
        updater()
        print(ThreadDone(CONNECTOR, NAME))
        await asyncio.sleep(INTERVAL)

def main():
    print(ThreadInitialized(CONNECTOR, NAME, VERSION))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(interval())
