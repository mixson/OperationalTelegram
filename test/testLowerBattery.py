from utils.Web_Rcs import Web_RCS
from utils import Paramiko_SSH

import json

if __name__ == '__main__':
    loginService = Web_RCS.LoginService()
    loginService.runService()

    agvStatus = Web_RCS.AGVStatusService()
    agvStatus.selectAGV(7118)
    result = agvStatus.sendJSON()
    agvStatusDict = json.loads(result.text)["data"][0]
    ip = agvStatusDict["robotIp"]

    ssh = Paramiko_SSH.LowerBatteryService()
    ssh.setAGVIP(ip)
    ssh.resumeNormalBattery()
    ssh.sendJSON()

    print("")