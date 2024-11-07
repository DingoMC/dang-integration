from models.skarpa.recalc_trigger import RecalcTrigger
from utils.console import ThreadCheckingNoNeed, ThreadInitialized, ThreadRunning, ThreadDone
from models.skarpa.user import User
from models.skarpa.season import Season
from models.skarpa.speed_score import SpeedScore
from models.skarpa.lead_score import LeadScore
from models.skarpa.bouldering_score import BoulderingScore
from models.skarpa.season_score import SeasonScore
import asyncio

VERSION = '0.3.0'
CONNECTOR = '<DB>'
NAME = 'skarpa.update.season_score'
INTERVAL = 600
# DELAY indicates that this task should be ran after others
DELAY = 15
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def updatePlace(season_scores : list[dict]):
    new_scores = sorted(season_scores, key=lambda ls: float(ls['p200']), reverse=True)
    out = 0
    for i in range(0, len(new_scores)):
        if bool(new_scores[i]['in_council']) == True:
            new_scores[i].update({"place": int(i+1-out)})
        else:
            out += 1
            new_scores[i].update({"place": int(-1)})
    return new_scores

def updatePlaceG(season_scores : list[dict]):
    scores_women = sorted([l for l in season_scores if bool(l['gender']) == False], key=lambda ls: float(ls['p200']), reverse=True)
    scores_men = sorted([l for l in season_scores if bool(l['gender']) == True], key=lambda ls: float(ls['p200']), reverse=True)
    out_w = 0
    out_m = 0
    for i in range(0, len(scores_women)):
        if bool(scores_women[i]['in_council']) == True:
            scores_women[i].update({"place_g": int(i+1-out_w)})
        else:
            out_w += 1
            scores_women[i].update({"place_g": int(-1)})
    for i in range(0, len(scores_men)):
        if bool(scores_men[i]['in_council']) == True:
            scores_men[i].update({"place_g": int(i+1-out_m)})
        else:
            out_m += 1
            scores_men[i].update({"place_g": int(-1)})
    return scores_women + scores_men

def checkTrigger():
    trigger = RecalcTrigger.select(filter=['value'],where={"type": "season"})
    if len(trigger) == 0:
        return False
    return bool(trigger[0][0])

def updater():
    users = User.select(['id', 'gender', 'in_council'])
    seasons = Season.select(['id'])
    for s in seasons:
        s_scores : list[dict] = []
        for u in users:
            ldata = LeadScore.select(['ls.p200'], {"ls.user_id": u[0], "s.id": s[0]}, ['Competition', 'Season'])
            sdata = SpeedScore.select(['ss.p200'], {"ss.user_id": u[0], "s.id": s[0]}, ['Competition', 'Season'])
            bdata = BoulderingScore.select(['blds.p200'], {"blds.user_id": u[0], "s.id": s[0]}, ['Competition', 'Season'])
            if len(ldata) > 0 or len(sdata) > 0 or len(bdata) > 0:
                total_p200 = 0.0
                if len(ldata) > 0:
                    total_p200 += float(ldata[0][0])
                if len(sdata) > 0:
                    total_p200 += float(sdata[0][0])
                if len(bdata) > 0:
                    total_p200 += float(bdata[0][0]) 
                s_scores.append({"user_id": u[0], "gender": bool(u[1]), "in_council": bool(u[2]), "season_id": s[0], "p200": total_p200})
        s_scores = updatePlace(s_scores)
        s_scores = updatePlaceG(s_scores)
        for ss in s_scores:
            SeasonScore.upsert(
                {"p200": ss['p200'], "place": ss['place'], "place_g": ss['place_g']},
                ['user_id', 'season_id', 'p200', 'place', 'place_g'],
                [ss['user_id'], ss['season_id'], ss['p200'], ss['place'], ss['place_g']],
                ['user_id', 'season_id']
            )
    RecalcTrigger.updateRow({"value": "false", "updated_at": "NOW()"}, {"type": "season"})
    RecalcTrigger.updateRow({"value": "true"}, {"type": "general"})

async def interval():
    await asyncio.sleep(DELAY)
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Checking if seasons need recalc'))
        update = checkTrigger()
        if update:
            print(ThreadRunning(CONNECTOR, NAME, 'Updating Season Score'))
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
