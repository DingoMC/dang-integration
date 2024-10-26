import requests
from utils.console import ErrorAPI

VERSION = "0.1.2"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def GetNameByUUID (uuid: str):
    api_url = 'https://sessionserver.mojang.com/session/minecraft/profile/' + uuid
    try:
        r = requests.get(api_url).json()
        name = r['name']
        return str(name)
    except:
        print(ErrorAPI(api_url))
        return ''
        
def GetUUIDByName (name: str):
    api_url = 'https://api.mojang.com/users/profiles/minecraft/' + name
    try:
        r = requests.get(api_url).json()
        uuid = r['id']
        return str(uuid)
    except:
        print(ErrorAPI(api_url))
        return ''
    
def GetServerInfo (dns : str):
    api_url = 'https://api.minetools.eu/ping/' + dns
    try:
        r = requests.get(api_url).json()
        return r
    except:
        print(ErrorAPI(api_url))
        return None

def dashedUUID (mcuuid: str):
    return mcuuid[0:8] + '-' + mcuuid[8:12] + '-' + mcuuid[12:16] + '-' + mcuuid[16:20] + '-' + mcuuid[20:]