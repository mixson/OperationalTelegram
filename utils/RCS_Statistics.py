from utils.Web_Rcs_14_04_22 import Web_RCS
import json


class StagingInfoService():

    # getting the active time of staging function
    # get staging info from RCS
    def __init__(self):
        self.mapDataService = Web_RCS.MapDataService()
        # self.mainTaskService = Web_RCS.TaskOrderService()
        # self.subTaskService = RCSOracleDataBase.SubTaskOrderService()
        # self.bjTaskService = BJTaskMsgService()
        # self.taskDict = {}
        #
        # self.dateTimeFormat = CONSTANT.DATETIME_FORMAT
        self.__login()

    def setMainTaskService(self, mainTaskService):
        self.mainTaskService = mainTaskService
        return self

    def setSubTaskService(self, subTaskService):
        self.subTaskService = subTaskService
        return self

    def setBjTaskService(self, bjTaskService):
        self.bjTaskService = bjTaskService
        return self

    def __login(self):
        rcs = Web_RCS()
        loginService = rcs.getLoginService()
        loginService.runService()

    def getStagingTimeList(self):
        pass


    def __setMapDataServiceInfo(self):
        self.mapDataService.selectPointType(34)  # 34 --> Pod Buffer X
        return self

    def __getStagingTotalAmountGoods(self, rackIdList):
        pass


    def __getExecutingTaskId(self, rackIdList):
        pass

    def getWorkingStagingDict(self):
        assert self.mapDataService
        self.__setMapDataServiceInfo()
        response = self.mapDataService.sendJSON()
        mapDataList = json.loads(response.text)["data"]
        total = len(mapDataList)
        workingStaging = 0
        for mapInfo in mapDataList:
            if "podCode" in mapInfo.keys():
                workingStaging += 1

        resultDict = {"total": total, "num": workingStaging}
        return resultDict

    def getWorkingStagingInfo(self):
        assert self.mapDataService
        self.__setMapDataServiceInfo()
        response = self.mapDataService.sendJSON()
        mapDataList = json.loads(response.text)["data"]
        total = len(mapDataList)
        workingStaging = 0
        for mapInfo in mapDataList:
            if "podCode" in mapInfo.keys():
                workingStaging += 1

        text = "Staging:\n"

        text += "Working: {}/{}".format(workingStaging, total)

        return text


if __name__ == "__main__":
    stagingInfoServiceHi = StagingInfoService()
    msg = stagingInfoServiceHi.getWorkingStagingDict()
    print("")