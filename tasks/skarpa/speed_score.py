from models.skarpa.recalc_trigger import RecalcTrigger
from utils.console import ThreadCheckingNoNeed, ThreadInitialized, ThreadRunning, ThreadDone
from models.skarpa.user import User
from models.skarpa.competition import Competition
from models.skarpa.speed_day_score import SpeedDayScore
from models.skarpa.speed_day import SpeedDay
from models.skarpa.speed_score import SpeedScore
from utils.linreg import LinearRegression
from dingorm import ExecuteSkarpaSQLUpdate
import asyncio

VERSION = '0.3.1'
CONNECTOR = '<DB>'
NAME = 'skarpa.update.speed_score'
INTERVAL = 600
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def calculateUserAtt(t_count : int, c_count : int, max_trains : int, max_comps : int):
    return 1.0 - ((max_trains - t_count) * 0.01 + (max_comps - c_count) * 0.1)

def updateP200(speed_scores : list[dict]):
    new_scores = speed_scores
    min_time = 99999.99
    for s in speed_scores:
        if s['avg'] is not None and float(s['avg']) < min_time:
            min_time = float(s['avg'])
    for i in range(0, len(new_scores)):
        if new_scores[i]['avg'] is not None:
            score = float(new_scores[i]['avg'])
            att_coeff = float(new_scores[i]['att_coeff'])
            new_scores[i].update({"p200": att_coeff * 200.0 * min_time / score})
        else:
            new_scores[i].update({"p200": 0.0})
    return new_scores

def updatePlace(speed_scores : list[dict]):
    new_scores = sorted(speed_scores, key=lambda ls: float(ls['p200']), reverse=True)
    for i in range(0, len(new_scores)):
        new_scores[i].update({"place": int(i+1)})
    return new_scores

def updatePlaceG(speed_scores : list[dict]):
    scores_women = sorted([l for l in speed_scores if bool(l['gender']) == False], key=lambda ls: float(ls['p200']), reverse=True)
    scores_men = sorted([l for l in speed_scores if bool(l['gender']) == True], key=lambda ls: float(ls['p200']), reverse=True)
    for i in range(0, len(scores_women)):
        scores_women[i].update({"place_g": int(i+1)})
    for i in range(0, len(scores_men)):
        scores_men[i].update({"place_g": int(i+1)})
    return scores_women + scores_men

def countDataColumn(raw_sdata : list[list], columnIndex: int, condition: int):
    cnt = 0
    for d in raw_sdata:
        if int(d[columnIndex]) == condition:
            cnt += 1
    return cnt

def averageColumn(raw_sdata : list[list], columnIndex: int):
    avg = 0.0
    for d in raw_sdata:
        avg += float(d[columnIndex])
    return avg / len(raw_sdata)

def generateProgressData(raw_sdata : list[list]):
    progress_data : list[list] = []
    for d in raw_sdata:
        # Take progress_x and average
        progress_data.append([d[0], d[1]])
    return progress_data

def checkTrigger():
    trigger = RecalcTrigger.select(filter=['value'],where={"type": "speed"})
    if len(trigger) == 0:
        return False
    return bool(trigger[0][0])

def updater():
    # Execute raw query updating averages for each day
    ExecuteSkarpaSQLUpdate('UPDATE "SpeedDayScore" SET average = CASE WHEN (time_a IS NULL AND time_b IS NULL) THEN NULL WHEN (time_a IS NULL) THEN time_b WHEN (time_b IS NULL) THEN time_a ELSE (time_a + time_b) / 2.0 END')
    users = User.select(['id', 'gender'])
    speed_comps = Competition.select(filter=['id'], where={"type": "s"})
    for sc in speed_comps:
        speed_scores : list[dict] = []
        max_data = SpeedDay.select(
            filter=['SUM(CAST(NOT is_comp AS INTEGER))', '(SUM(CAST(is_comp AS INTEGER)) / 3)'],
            where={"competition_id": sc[0]}
        )
        max_trains = 0
        max_comps = 0
        if len(max_data) > 0:
            max_trains = int(max_data[0][0])
            max_comps = int(max_data[0][1])
        for u in users:
            data = SpeedDayScore.select(
                filter=['sd.progress_x', 'sds.average', 'CAST(sd.is_comp AS INTEGER)'],
                where={"sds.user_id": u[0], "sd.competition_id": sc[0]},
                join=['SpeedDay']
            )
            if len(data) > 0:
                avg = averageColumn(data, 1)
                t_count = countDataColumn(data, 2, 0)
                c_count = countDataColumn(data, 2, 1) // 3
                att_coeff = calculateUserAtt(t_count, c_count, max_trains, max_comps)
                progress_data = generateProgressData(data)
                linreg = LinearRegression(progress_data)
                temp = {"user_id": u[0], "gender": bool(u[1]), "competition_id": sc[0], "trains": t_count, "comps": c_count, "att_coeff": att_coeff, "avg": avg}
                if linreg is not None:
                    temp.update({"progress": -linreg.byx})
                else:
                    temp.update({"progress": 0.0})
                speed_scores.append(temp)
        speed_scores = updateP200(speed_scores)
        speed_scores = updatePlace(speed_scores)
        speed_scores = updatePlaceG(speed_scores)
        for ss in speed_scores:
            SpeedScore.upsert(
                {"trains": ss['trains'], "comps": ss['comps'], "att_coeff": ss['att_coeff'], "average": ss['avg'], "progress": ss['progress'], "p200": ss['p200'], "place": ss['place'], "place_g": ss['place_g']},
                ['trains', 'comps', 'att_coeff', 'average', 'progress', 'p200', 'place', 'place_g', 'user_id', 'competition_id'],
                [ss['trains'], ss['comps'], ss['att_coeff'], ss['avg'], ss['progress'], ss['p200'], ss['place'], ss['place_g'], ss['user_id'], ss['competition_id']],
                ['user_id', 'competition_id']
            )
    RecalcTrigger.updateRow({"value": "false", "updated_at": "NOW()"}, {"type": "speed"})
    RecalcTrigger.updateRow({"value": "true"}, {"type": "season"})

async def interval():
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Checking if speed needs recalc'))
        update = checkTrigger()
        if update:
            print(ThreadRunning(CONNECTOR, NAME, 'Updating Speed Score'))
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
