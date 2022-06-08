from utils.Web_Rcs_14_04_22 import Web_RCS

if __name__ == '__main__':
    loginService = Web_RCS.LoginService()
    loginService.runService()
    resumePauseAGVService = Web_RCS.AGVStatusService()
    resumePauseAGVService.selectAGV(7118)
    result = resumePauseAGVService.sendJSON()
    print(result.text)
    print("")