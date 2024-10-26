from models.mcserverinfo import MCServerInfo
from utils.mcapi import GetServerInfo
from utils.console import ThreadInitialized, ThreadRunning, ThreadDone, WarningUpdateServerInfo, WarningServerInfoInvalid
import asyncio

VERSION = '0.1.0'
CONNECTOR = 'API->DB'
NAME = 'dang$$.serverinfo.update'
INTERVAL = 600
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def updater():
    dns = 'dingo-mc.net'
    data = GetServerInfo(dns)
    if data is None:
        print(WarningUpdateServerInfo(dns))
        return
    description = ""
    latency = 0
    players = 0
    players_max = 0
    sample = "None"
    version = ""
    try:
        description = str(data['description'])
        latency = int(data['latency'])
        players = int(data['players']['online'])
        players_max = int(data['players']['max'])
        raw_sample = list(data['players']['sample'])
        version = str(data['version']['name'])
        if len(raw_sample) > 0:
            sample = ','.join(raw_sample)
    except:
        print(WarningServerInfoInvalid(dns))
        return
    MCServerInfo.updateRow({
        "description": description,
        "latency": latency,
        "players": players,
        "players_max": players_max,
        "sample": sample,
        "version": version},
        {"dns": dns})

async def interval():
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Updating Server Info'))
        updater()
        print(ThreadDone(CONNECTOR, NAME))
        await asyncio.sleep(INTERVAL)

def main():
    print(ThreadInitialized(CONNECTOR, NAME, VERSION))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(interval())
