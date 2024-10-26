from models.skarpa.recalc_trigger import RecalcTrigger
from utils.console import ThreadCheckingNoNeed, ThreadInitialized, ThreadRunning, ThreadDone
from models.skarpa.user import User
from dingorm import ExecuteSkarpaSQL
import asyncio

VERSION = '0.2.0'
CONNECTOR = '<DB>'
NAME = 'skarpa.update.general_score'
INTERVAL = 600
# DELAY indicates that this task should be ran after others
DELAY = 30
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def updatePlaceG(general_scores : list[dict]):
    scores_women = sorted([l for l in general_scores if bool(l['gender']) == False], key=lambda ls: float(ls['p200']), reverse=True)
    scores_men = sorted([l for l in general_scores if bool(l['gender']) == True], key=lambda ls: float(ls['p200']), reverse=True)
    for i in range(0, len(scores_women)):
        scores_women[i].update({"place": int(i+1)})
    for i in range(0, len(scores_men)):
        scores_men[i].update({"place": int(i)})
    return scores_women + scores_men

def checkTrigger():
    trigger = RecalcTrigger.select(filter=['value'],where={"type": "general"})
    if len(trigger) == 0:
        return False
    return bool(trigger[0][0])

def updater():
    # Custom Fetch summed up P200 for each user
    data = ExecuteSkarpaSQL('SELECT SUM(ss.p200), ss.user_id, u.gender FROM public."SeasonScore" ss LEFT JOIN public."User" u ON u.id = ss.user_id GROUP BY ss.user_id, u.gender')
    gdata : list[dict] = []
    for d in data:
        gdata.append({"p200": d[0], "user_id": d[1], "gender": d[2]})
    gdata = updatePlaceG(gdata)
    for g in gdata:
        User.updateRow({"p200": g['p200'], "place": g['place']}, {"id": g['user_id']})
    RecalcTrigger.updateRow({"value": "false", "updated_at": "NOW()"}, {"type": "general"})

async def interval():
    await asyncio.sleep(DELAY)
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Checking if general score needs recalc'))
        update = checkTrigger()
        if update:
            print(ThreadRunning(CONNECTOR, NAME, 'Updating General Score'))
            updater()
            print(ThreadDone(CONNECTOR, NAME))
        else:
            print(ThreadCheckingNoNeed(CONNECTOR, NAME))
        await asyncio.sleep(INTERVAL)

def main():
    print(ThreadInitialized(CONNECTOR, NAME, VERSION))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(interval())
