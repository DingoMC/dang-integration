"""dang$$ Minecraft Connector

This module contains Minecraft data handling/conversion
Created by: DingoMC
Cores: akka, umbry

"""
from nbt import nbt
from utils.console import MCConNoScore, MCConFoundScore, MCConErrNoPath
VERSION = "1.0.1"
NO_SCORE = -2147483647
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
def GetScore (Path : str, Name : str, Objective : str):
    r"""[ dang$$ umbry ]

    Gets score of a player from objective from nbt file

    Parameters
    -----------
    Path: str
        Path to NBT file
    Name: str
        Player in-game name
    Objective: str
        Objective name

    Returns
    --------
    Int: Score
    """
    try:
        nbt_file = nbt.NBTFile(Path, 'rb')
    except:
        print(MCConErrNoPath(Path))
        return NO_SCORE
    else:
        for i in range (0, len(nbt_file['data']['PlayerScores']), 1):
            if str(nbt_file['data']['PlayerScores'][i]['Name']) == Name:
                if str(nbt_file['data']['PlayerScores'][i]['Objective']) == Objective:
                    score = str(nbt_file['data']['PlayerScores'][i]['Score'])
                    print(MCConFoundScore(Name, Objective, score))
                    return int(score)
        print(MCConNoScore(Name, Objective))
        return NO_SCORE

def GetColor (prefix: str):
    if prefix == '0': return 0x000000
    if prefix == '1': return 0x0000aa
    if prefix == '2': return 0x00aa00
    if prefix == '3': return 0x00aaaa
    if prefix == '4': return 0xaa0000
    if prefix == '5': return 0xaa00aa
    if prefix == '6': return 0xffaa00
    if prefix == '7': return 0xaaaaaa
    if prefix == '8': return 0x555555
    if prefix == '9': return 0x5555ff
    if prefix == 'a': return 0x55ff55
    if prefix == 'b': return 0x55ffff
    if prefix == 'c': return 0xff5555
    if prefix == 'd': return 0xff55ff
    if prefix == 'e': return 0xffff55
    return 0xffffff

def GetJSONColor (prefix: str):
    if prefix == '0': return 'black'
    if prefix == '1': return 'dark_blue'
    if prefix == '2': return 'dark_green'
    if prefix == '3': return 'dark_aqua'
    if prefix == '4': return 'dark_red'
    if prefix == '5': return 'dark_purple'
    if prefix == '6': return 'gold'
    if prefix == '7': return 'gray'
    if prefix == '8': return 'dark_gray'
    if prefix == '9': return 'blue'
    if prefix == 'a': return 'green'
    if prefix == 'b': return 'aqua'
    if prefix == 'c': return 'red'
    if prefix == 'd': return 'light_purple'
    if prefix == 'e': return 'yellow'
    return 'white'
