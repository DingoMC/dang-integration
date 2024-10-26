from models.mcuser import MCUser
from models.minigames_points import MinigamesPoints
from models.minigames import Minigames
from utils.mccon import GetScore, NO_SCORE
from utils.console import ThreadInitialized, ThreadRunning, ThreadDone
import asyncio

VERSION = '0.1.2'
CONNECTOR = 'MC->DB'
NAME = 'dang$$.minigames.points.update'
INTERVAL = 600
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def updater():
    data = MCUser.select(['uuid', 'mcuuid', 'name'])
    mdata = Minigames.select(['id', 'objective'])
    for user in data:
        m_scores = []
        m_ids = []
        for j in mdata:
            m_ids.append(j[0])
            if j[0] == 4:
                m_scores.append(0)
            else:
                score = GetScore('/root/minecraft_m/minigames/data/scoreboard.dat', user[2], j[1])
                if score > NO_SCORE:
                    m_scores.append(score)
                else:
                    m_scores.append(0)
        MinigamesPoints.updateColumn('points', 'minigame_id', m_scores, m_ids, {"uuid": user[0]})

async def interval():
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Updating minigames points'))
        updater()
        print(ThreadDone(CONNECTOR, NAME))
        await asyncio.sleep(INTERVAL)

def main():
    print(ThreadInitialized(CONNECTOR, NAME, VERSION))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(interval())
