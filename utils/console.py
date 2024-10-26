"""dang$$ Console

This module contains Console handling
Created by: DingoMC
Cores: akka, umbry

"""
from datetime import datetime

VERSION = "0.1.5"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def CS(text : str, color : str):
    final_text = "\033[0;3"
    if color == "red" or color == "r":
        final_text += "1m"
    elif color == "green" or color == "g":
        final_text += "2m"
    elif color == "yellow" or color == "y":
        final_text += "3m"
    elif color == "blue" or color == "b":
        final_text += "4m"
    elif color == "purple" or color == "p":
        final_text += "5m"
    elif color == "cyan" or color == "c":
        final_text += "6m"
    elif color == "gray":
        final_text += "7m"
    else:
        final_text += "9m"
    final_text += text
    final_text += "\033[0;39m"
    return final_text
# dang$$ Flags
DAT = CS(' > ', "cyan")     # at
DARR = CS(' -> ', "y")      # arrow
COL = CS(' : ',"cyan")      # subseq
ACK = CS('ACK',"g")        # ACK
RST = CS('RST ',"r")        # Reset
ERR = CS('ERR',"r")        # Error
WARN = CS('WARN', "y")      # Warning
SET = CS('SET ',"y")        # Setup
INI = CS('INIT',"r")        # Init
DCALL = CS('CALL',"y")      # Call
TASK = CS('TASK',"p")       # Task
LST = CS('LST ',"cyan")     # Listener
LOAD = CS('LOAD',"r")       # Imports
END = CS('END',"r")         # End
SQL = CS('SQL', "b")        # SQL

def prtime ():
    ctime = datetime.now()
    cts = ctime.strftime("[%d/%m/%Y][%H:%M:%S]")
    return CS(cts, 'gray')
def prefix ():
    return CS('[dang$$]',"r")
def tprefix ():
    return prtime() + prefix() + ' '
def ThreadInitializing (name : str):
    return tprefix() + INI + COL + 'Initializing Thread' + COL + CS(name, "y") + '...'
def ThreadInitialized (connector : str, name : str, version : str):
    return tprefix() + ACK + COL + 'Initialized Thread' + COL + CS(connector + ' ' + name + ' ' + version, "g") + '.'
def ThreadCheckingNoNeed (connector : str, name : str):
    return tprefix() + ACK + DAT + CS(connector + ' ' + name, "g") + COL + 'No need for recalc. Skipping.'
def ThreadRunning (connector : str, name : str, action : str):
    return tprefix() + DCALL + DAT + CS(connector + ' ' + name, "g") + COL + action + '...'
def ThreadDone (connector : str, name : str):
    return tprefix() + ACK + DAT + CS(connector + ' ' + name, "g") + COL + 'Done.'
def ProgramExit ():
    return tprefix() + END
def ProgramInit (version : str):
    return tprefix() + INI + COL + 'Initializing dang$$ integrator v.' + version + '.'
def DingormExec (sql : str):
    return tprefix() + SQL + DAT + CS('dingorm', "p") + COL + CS(sql, "b")
def ErrorAPI (url : str):
    return tprefix() + ERR + COL + 'Error while calling: ' + CS(url, "cyan") + ' - request failed.'
def WarningUpdateServerInfo (dns : str):
    return tprefix() + WARN + COL + 'No server info provided from API for: ' + CS(dns, "cyan") + '.'
def WarningServerInfoInvalid (dns : str):
    return tprefix() + WARN + COL + 'Can\'t convert server info provided from API for: ' + CS(dns, "cyan") + '.'
def DingormErrorExecuteSQL(sql : str, err : str = None):
    if err is None:
        return tprefix() + ERR + DAT + CS('dingorm', "r") + COL + 'Unkown Error while executing SQL statement: ' + CS(sql, "r") + '.'
    return tprefix() + ERR + DAT + CS('dingorm', "r") + COL + 'SQL Error: ' + CS(err, "r")
def InitBox(version : str):
    lines : list[str] = [
        '\u250C\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502\t\t\t\t\u2502',
        '\u2502\t' + CS('dang$$', "r") + ' ' + CS('Integrator', "cyan") + '\t\u2502',
        '\u2502\t' + CS('Version', "g") + ': ' + CS(version, "p") + '\t\t\u2502',
        '\u2502\t\t\t\t\u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518'
    ]
    return '\n'.join(lines)
def MCConErrNoPath(path : str):
    return tprefix() + ERR + DAT + CS('mccon', "r") + COL + 'Invalid path for NBT file: ' + CS(path, "r") + '.'
def MCConNoScore(name : str, objective : str):
    return tprefix() + WARN + DAT + CS('mccon', "y") + COL + 'No score found for player: ' + CS(name, "y") + ' in objective: ' + CS(objective, "y") + '.'
def MCConFoundScore(name : str, objective : str, score : int):
    return tprefix() + ACK + DAT + CS('mccon', "p") + COL + 'Name: ' + CS(name, "cyan") + ', Objective: ' + CS(objective, "cyan") + ', Score: ' + CS(str(score), "cyan") + '.'