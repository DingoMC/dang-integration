from utils.console import ThreadInitialized, ThreadRunning, ThreadDone, ThreadCheckingNoNeed
from models.skarpa.user import User
from models.skarpa.competition import Competition
from models.skarpa.boulder_week_score import BoulderWeekScore
from models.skarpa.bouldering_score import BoulderingScore
from models.skarpa.recalc_trigger import RecalcTrigger
from utils.linreg import LinearRegression
from dingorm import ExecuteSkarpaSQLUpdate, ExecuteSkarpaSQL
import asyncio

VERSION = '0.4.0'
CONNECTOR = '<DB>'
NAME = 'skarpa.update.bouldering_score'
INTERVAL = 600
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def updateP200(bouldering_scores : list[dict]):
    new_scores = bouldering_scores
    max_score = 0.0
    for s in bouldering_scores:
        if s['score_m'] is not None and bool(s['in_council']) == True and float(s['score_m']) > max_score:
            max_score = float(s['score_m'])
    for i in range(0, len(new_scores)):
        if new_scores[i]['score_m'] is not None:
            if bool(new_scores[i]['in_council']) == True:
                score = float(new_scores[i]['score_m'])
                new_scores[i].update({"p200": score * 200.0 / max_score})
            else:
                new_scores[i].update({"p200": 0.0})
    return new_scores

def updateP200Generic(bouldering_scores : list[dict]):
    new_scores = bouldering_scores
    max_score = 0.0
    for s in bouldering_scores:
        if s['score_m'] is not None and float(s['score_m']) > max_score:
            max_score = float(s['score_m'])
    for i in range(0, len(new_scores)):
        if new_scores[i]['score_m'] is not None:
            score = float(new_scores[i]['score_m'])
            new_scores[i].update({"p200_generic": score * 200.0 / max_score})
    return new_scores

def updatePlace(bouldering_scores : list[dict]):
    new_scores = sorted(bouldering_scores, key=lambda ls: float(ls['score_m']), reverse=True)
    out = 0
    for i in range(0, len(new_scores)):
        if bool(new_scores[i]['in_council']) == True:
            new_scores[i].update({"place": int(i+1-out)})
        else:
            out += 1
            new_scores[i].update({"place": int(-1)})
    return new_scores

def updatePlaceG(bouldering_scores : list[dict]):
    scores_women = sorted([l for l in bouldering_scores if bool(l['gender']) == False], key=lambda ls: float(ls['score_m']), reverse=True)
    scores_men = sorted([l for l in bouldering_scores if bool(l['gender']) == True], key=lambda ls: float(ls['score_m']), reverse=True)
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

def generateProgressData(raw_bdata : list[list]):
    progress_data : list[list] = []
    for d in raw_bdata:
        # Take progress_x and score_m
        progress_data.append([d[0], d[2]])
    return progress_data

def sumDataColumn(raw_bdata : list[list], columnIndex: int):
    sum = 0.0
    for d in raw_bdata:
        sum += float(d[columnIndex])
    return sum

def checkTrigger():
    trigger = RecalcTrigger.select(filter=['value'],where={"type": "bouldering"})
    if len(trigger) == 0:
        return False
    return bool(trigger[0][0])

def updater():
    # Execute raw query updating relative difficulty for each boulder
    ExecuteSkarpaSQLUpdate('UPDATE public."Boulder" b SET relative_diff = (CAST(b.level AS FLOAT) / CAST(bw.boulder_count AS FLOAT)) FROM public."BoulderWeek" bw WHERE bw.id = b.boulder_week_id;')
    # Execute raw query updating true difficulty for each boulder
    ExecuteSkarpaSQLUpdate('WITH x AS (SELECT boulder_id, ((3.0 * COUNT(score) - SUM(score)) / (3.0 * COUNT(score))) AS true_diff FROM public."BoulderScore" GROUP BY boulder_id) UPDATE public."Boulder" b SET true_diff = x.true_diff FROM x WHERE b.id = x.boulder_id')
    # Execute raw query updating difficulty coefficient for each boulder
    ExecuteSkarpaSQLUpdate('WITH x AS (SELECT boulder_week_id, relative_diff AS diff1 FROM public."Boulder" WHERE level = 1) UPDATE public."Boulder" b SET diff_coeff = (1.0 + LN(1.0 - x.diff1 + (b.relative_diff + b.true_diff) * 0.5)) FROM x WHERE x.boulder_week_id = b.boulder_week_id')
    # Execute raw query updating is_top and is_flash columns
    ExecuteSkarpaSQLUpdate('UPDATE public."BoulderScore" SET is_top = (score >= 1), is_flash = (score = 3)')
    # Execute raw query to calculate boulder week score data
    bw_data = ExecuteSkarpaSQL('SELECT b.boulder_week_id, bs.user_id, SUM(bs.score) AS score, SUM((bs.score * b.diff_coeff)) AS score_m, SUM(CAST(bs.is_top AS INTEGER)) AS tops, SUM(CAST(bs.is_flash AS INTEGER)) AS flashes FROM public."BoulderScore" bs LEFT JOIN public."Boulder" b ON bs.boulder_id = b.id GROUP BY b.boulder_week_id, bs.user_id')
    # Upsert BoulderWeekScore Table
    for bwd in bw_data:
        BoulderWeekScore.upsert(
            {"score": bwd[2], "score_m": bwd[3], "tops": bwd[4], "flashes": bwd[5]},
            ['boulder_week_id', 'user_id', 'score', 'score_m', 'tops', 'flashes'],
            bwd,
            ['boulder_week_id', 'user_id']
        )
    users = User.select(['id', 'gender', 'in_council'])
    bouldering_comps = Competition.select(filter=['id'], where={"type": "b"})
    for bc in bouldering_comps:
        b_scores : list[dict] = []
        for u in users:
            data = BoulderWeekScore.select(
                filter=['bw.progress_x', 'bws.score', 'bws.score_m', 'bws.tops', 'bws.flashes'],
                where={"bws.user_id": u[0], "bw.competition_id": bc[0]},
                join=['BoulderWeek']
            )
            if len(data) > 0:
                progress_data = generateProgressData(data)
                linreg = LinearRegression(progress_data)
                temp = {
                    "user_id": u[0], "gender": bool(u[1]), "in_council": bool(u[2]), "competition_id": bc[0],
                    "score": sumDataColumn(data, 1),
                    "score_m": sumDataColumn(data, 2),
                    "tops": int(sumDataColumn(data, 3)),
                    "flashes": int(sumDataColumn(data, 4))
                }
                if linreg is not None:
                    temp.update({"progress": linreg.byx})
                else:
                    temp.update({"progress": 0.0})
                b_scores.append(temp)
        b_scores = updateP200(b_scores)
        b_scores = updateP200Generic(b_scores)
        b_scores = updatePlace(b_scores)
        b_scores = updatePlaceG(b_scores)
        for bs in b_scores:
            BoulderingScore.upsert(
                {"flashes": bs['flashes'], "tops": bs['tops'], "score": bs['score'], "progress": bs['progress'], "score_m": bs['score_m'], "p200": bs['p200'], "p200_generic": bs['p200_generic'], "place_g": bs['place_g'], "place": bs['place']},
                ['user_id', 'competition_id', 'flashes', 'tops', 'score', 'progress', 'score_m', 'p200', 'p200_generic', 'place_g', 'place'],
                [bs['user_id'], bs['competition_id'], bs['flashes'], bs['tops'], bs['score'], bs['progress'], bs['score_m'], bs['p200'], bs['p200_generic'], bs['place_g'], bs['place']],
                ['user_id', 'competition_id']
            )
    RecalcTrigger.updateRow({"value": "false", "updated_at": "NOW()"}, {"type": "bouldering"})
    RecalcTrigger.updateRow({"value": "true"}, {"type": "season"})

async def interval():
    while True:
        print(ThreadRunning(CONNECTOR, NAME, 'Checking if bouldering needs recalc'))
        update = checkTrigger()
        if update:
            print(ThreadRunning(CONNECTOR, NAME, 'Updating Bouldering Score'))
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
