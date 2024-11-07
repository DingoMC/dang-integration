from models.skarpa.recalc_trigger import RecalcTrigger
from utils.console import ThreadCheckingNoNeed, ThreadInitialized, ThreadRunning, ThreadDone
from models.skarpa.user import User
from models.skarpa.competition import Competition
from models.skarpa.lead_score import LeadScore
from models.skarpa.lead_route_score import LeadRouteScore
import asyncio

VERSION = '0.3.1'
CONNECTOR = '<DB>'
NAME = 'skarpa.update.lead_score'
INTERVAL = 600
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def calculateUserScore(data : list[list]):
    if len(data) == 0:
        return 0.0
    total = 0.0
    for d in data:
        level = int(d[0])
        is_circle = bool(d[1])
        score = float(d[2])
        score_ceil = 0
        if d[3] is not None:
            score_ceil = float(d[3])
        score_lead = 0
        if d[4] is not None:
            score_lead = float(d[4])
        score_expr = 0
        if d[5] is not None:
            score_expr = float(d[5])
        if is_circle:
            total += score * level
        elif level == 1:
            total += score
        elif level == 2:
            total += score_ceil
        elif level == 3:
            total += score_lead
        else:
            total += score_expr
    return total

def updateP200(lead_scores : list[dict]):
    new_scores = lead_scores
    max_score = 0.0
    for s in lead_scores:
        if s['score'] is not None and bool(s['in_council']) == True and float(s['score']) > max_score:
            max_score = float(s['score'])
    for i in range(0, len(new_scores)):
        if new_scores[i]['score'] is not None:
            score = float(new_scores[i]['score'])
            if bool(new_scores[i]['in_council']) == True:
                new_scores[i].update({"p200": score * 200.0 / max_score})
            else:
                new_scores[i].update({"p200": 0})
    return new_scores

def updatePlace(lead_scores : list[dict]):
    new_scores = sorted(lead_scores, key=lambda ls: float(ls['score']), reverse=True)
    out = 0
    for i in range(0, len(new_scores)):
        if bool(new_scores[i]['in_council']) == True:
            new_scores[i].update({"place": int(i+1-out)})
        else:
            out += 1
            new_scores[i].update({"place": int(-1)})
    return new_scores

def updatePlaceG(lead_scores : list[dict]):
    scores_women = sorted([l for l in lead_scores if bool(l['gender']) == False], key=lambda ls: float(ls['score']), reverse=True)
    scores_men = sorted([l for l in lead_scores if bool(l['gender']) == True], key=lambda ls: float(ls['score']), reverse=True)
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
    trigger = RecalcTrigger.select(filter=['value'],where={"type": "lead"})
    if len(trigger) == 0:
        return False
    return bool(trigger[0][0])

def updater():
    users = User.select(['id', 'gender', 'in_council'])
    lead_comps = Competition.select(filter=['id'], where={"type": "l"})
    for lc in lead_comps:
        lead_scores : list[dict] = []
        for u in users:
            data = LeadRouteScore.select(
                filter=['lrs.level', 'lr.is_circle', 'lr.score', 'lr.score_ceil', 'lr.score_lead', 'lr.score_expr'],
                where={"lrs.user_id": u[0], "lr.competition_id": lc[0]},
                join=['LeadRoute'])
            if len(data) > 0:
                score = calculateUserScore(data)
                lead_scores.append({"user_id": u[0], "gender": bool(u[1]), "in_council": bool(u[2]), "competition_id": lc[0], "score": score})
        lead_scores = updateP200(lead_scores)
        lead_scores = updatePlace(lead_scores)
        lead_scores = updatePlaceG(lead_scores)
        for ls in lead_scores:
            LeadScore.upsert(
                {"score": ls['score'], "p200": ls['p200'], "place": ls['place'], "place_g": ls['place_g']},
                ['score', 'p200', 'place_g', 'place', 'user_id', 'competition_id'],
                [ls['score'], ls['p200'], ls['place_g'], ls['place'], ls['user_id'], ls['competition_id']],
                ['user_id', 'competition_id']
            )
    RecalcTrigger.updateRow({"value": "false", "updated_at": "NOW()"}, {"type": "lead"})
    RecalcTrigger.updateRow({"value": "true"}, {"type": "season"})

async def interval():
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Checking if lead needs recalc'))
        update = checkTrigger()
        if update:
            print(ThreadRunning(CONNECTOR, NAME, 'Updating Lead Score'))
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
