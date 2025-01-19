import multiprocessing
# import tasks.mcupdate_points as mcp
# import tasks.mcupdate_hours as mch
# import tasks.mcupdate_m_points as mcmp
import tasks.api_names as an
import tasks.api_serverinfo as asi
# import tasks.mcupdate_location as mcl
# import tasks.mcupdate_kdr as mck
import tasks.skarpa.lead_score as sls
import tasks.skarpa.speed_score as sss
import tasks.skarpa.bouldering_score as sbs
import tasks.skarpa.season_score as sses
import tasks.skarpa.general_score as sgs
from utils.console import ThreadInitializing, ProgramExit, ProgramInit, InitBox

VERSION = "0.3.9"

# Tasks class
class DangTask:
    def __init__ (self, name : str, thread : multiprocessing.Process):
        self.name = name
        self.thread = thread

def main():
    print(ProgramInit(VERSION))
    print(InitBox(VERSION))
    dangTasks : list[DangTask] = [
        DangTask(an.CONNECTOR + ' ' + an.NAME, multiprocessing.Process(target=an.main, daemon=True)),
        DangTask(asi.CONNECTOR + ' ' + asi.NAME, multiprocessing.Process(target=asi.main, daemon=True)),
        # DangTask(mcp.CONNECTOR + ' ' + mcp.NAME, multiprocessing.Process(target=mcp.main, daemon=True)),
        # DangTask(mch.CONNECTOR + ' ' + mch.NAME, multiprocessing.Process(target=mch.main, daemon=True)),
        # DangTask(mcmp.CONNECTOR + ' ' + mcmp.NAME, multiprocessing.Process(target=mcmp.main, daemon=True)),
        # DangTask(mcl.CONNECTOR + ' ' + mcl.NAME, multiprocessing.Process(target=mcl.main, daemon=True)),
        # DangTask(mck.CONNECTOR + ' ' + mck.NAME, multiprocessing.Process(target=mck.main, daemon=True)),
        DangTask(sls.CONNECTOR + ' ' + sls.NAME, multiprocessing.Process(target=sls.main, daemon=True)),
        DangTask(sss.CONNECTOR + ' ' + sss.NAME, multiprocessing.Process(target=sss.main, daemon=True)),
        DangTask(sbs.CONNECTOR + ' ' + sbs.NAME, multiprocessing.Process(target=sbs.main, daemon=True)),
        DangTask(sses.CONNECTOR + ' ' + sses.NAME, multiprocessing.Process(target=sses.main, daemon=True)),
        DangTask(sgs.CONNECTOR + ' ' + sgs.NAME, multiprocessing.Process(target=sgs.main, daemon=True))
    ]
    threads : list[multiprocessing.Process] = list()
    for dt in dangTasks:
        print(ThreadInitializing(dt.name))
        threads.append(dt.thread)
        dt.thread.start()

    for t in threads:
        t.join()
    print(ProgramExit())
    return 0

if __name__ == "__main__":
    main()