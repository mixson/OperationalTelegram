from utils.task_list import TaskDict
from values.CONSTANT import RCS_CONSTANT, AREA_COORDINATION_DIVIDE, CHARGING_STATION_COORDINATION, MainTaskStatusDict, COMBINED_STATION_DICT
from utils.General_Function import withInRange

import json
import requests as httpclient
import datetime
import re

# from utils import RCS_Statistics



class Web_RCS:
    SESSION = httpclient.Session()
    PROTOCOL = RCS_CONSTANT.PROTOCOL
    IP = RCS_CONSTANT.IP
    PORT = RCS_CONSTANT.PORT
    SYSTEM = RCS_CONSTANT.SYSTEM
    COOKIES = {"HIK_COOKIE": "",
                            "JSESSIONID": "",
                            "ecsElcMap": "1001%2CXY%3B1001%2CXY%3B0",
                            "ecsRemeber": "1%3Badmin",
                            "ecsSelectedMenu": "70",
                            "langTypeWdatePicker": "en"
                            }

    HEADERS = {"Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zhq=0.9",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded charset=UTF-8",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36\
                                 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest"}


    @staticmethod
    def getSystemURL():
        if Web_RCS.PROTOCOL and Web_RCS.IP and Web_RCS.PORT and Web_RCS.SYSTEM:
            return "{}://{}:{}/{}".format(Web_RCS.PROTOCOL, Web_RCS.IP, Web_RCS.PORT, Web_RCS.SYSTEM)

    @staticmethod
    def setPROTOCOL(protocol):
        Web_RCS.PROTOCOL = protocol
        return Web_RCS

    @staticmethod
    def setIP(ip):
        Web_RCS.IP = ip
        return Web_RCS

    @staticmethod
    def setPORT(port):
        Web_RCS.PORT = port
        return Web_RCS

    @staticmethod
    def setSystem(system):
        Web_RCS.SYSTEM = system
        return Web_RCS

    @staticmethod
    def getCookies():
        return Web_RCS.COOKIES

    @staticmethod
    def getHeaders():
        return Web_RCS.HEADERS

    @staticmethod
    def setCookies(cookies):
        Web_RCS.COOKIES = cookies
        return Web_RCS

    @staticmethod
    def setCookiesJSESSION(jsession):
        Web_RCS.COOKIES["JSESSIONID"] = jsession
        return Web_RCS

    @staticmethod
    def setCookiesHIKCOOKIES(hikcookies):
        Web_RCS.COOKIES["HIK_COOKIE"] = hikcookies
        return Web_RCS

    def __init__(self):
        self.service = {}



    def getService(self, serviceName):
        # if serviceName not in self.service.keys():
        #     self.service[serviceName] =
        return self.service[serviceName]

    def getLoginService(self):
        if "LoginService" not in self.service.keys():
            self.addServie(Web_RCS.LoginService())
        return self.getService("LoginService")

    def addServie(self, service):
        serviceName = service.__class__.__name__
        self.service[serviceName] = service
        return self

    class Service_Interface():
        def __init__(self):
            self.serviceLocation = ""
            self.params = {}

        def getServiceLocation(self):
            return self.serviceLocation

        def getDestination(self):
            return Web_RCS.getSystemURL() + self.getServiceLocation()

        def sendJSON(self):
            pass

    class LoginService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/login!login.action"
            self.parameter = {}

            self.ACCOUNT = "admin"
            # self.PWD = "c2e862d7b7840e1c15f85a6c3902efcf" # 26 Server pw
            self.PWD = "518bedf671377055e944f0bcf5efc005" # 30 Server

            self.COOKIES = {"HIK_COOKIE": "",
                            "JSESSIONID": "",
                            "ecsElcMap": "1001%2CXY%3B1001%2CXY%3B0",
                            "ecsRemeber": "0%3B",
                            "ecsDevice": "1001%2CXY%3B1001%2CXY",
                            "ecsSelectedMenu": "20",
                            "langTypeWdatePicker": "en"
                            }

            self.TOKEN = ""
            self.JSESSION = ""

            self.LOGINSTATUS = False


        def setAccount(self, account):
            self.ACCOUNT = account
            return self

        def setPWD(self, pwd):
            self.PWD = pwd
            return self


        def setToken(self, token):
            self.TOKEN = token
            return self

        def setJSESSION(self, JSESSION):
            self.JSESSION = JSESSION
            return self

        def getServiceLocation(self):
            return self.serviceLocation

        def getCookies(self):
            if Web_RCS.COOKIES["HIK_COOKIE"] == "" or Web_RCS.COOKIES["JSESSIONID"] == "":
                if self.TOKEN == "" or self.JSESSION == "":
                    raise Exception("'HIK_COOKIES/ JSESSIONID' variable(s) is empty}")
            Web_RCS.COOKIES["HIK_COOKIE"] = self.TOKEN
            Web_RCS.COOKIES["JSESSIONID"] = self.JSESSION
            return self.COOKIES

        def getHeaders(self):
            return Web_RCS.HEADERS

        def runService(self):
            if self.ACCOUNT == "" or self.PWD == "":
                raise Exception("Account/ Password is empty")

            loginDict = {"ecsUserName": self.ACCOUNT,
                         "ecsPassword": self.PWD,
                         "pwdSafeLevelLogin": 3}

            result = Web_RCS.SESSION.post(self.getDestination(), data=loginDict)
            print("Login Result: {}".format(result.text))
            if "User account or authorization expired." in result.text:
                print("Login is not successful")
                self.LOGINSTATUS = False
                return False
            # result["cookies"]["_cookies"][RCS.IP]["/{}/".format(RCS.SYSTEM)]
            self.LOGINSTATUS = True
            return True

        def checkLoginStatus(self):
            if self.TOKEN == "" or self.JSESSION == "":
                raise Exception("Please check JOKEN/ JSESSION: " + "{0}/ {1}".format(self.TOKEN, self.JSESSION))
            result = httpclient.post(self.getURL(), json="")
            if "User account or authorization expired." in result.text:
                print("Please check validation of token/ JSESSION" + "{0}/ {1}".format(self.TOKEN, self.JSESSION))
                return False
            return True


    class TaskDispatchService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/agvControl!genAgvSchedulingTask.action"
            # self.serviceLocation = "/web/agvTaskMgr.action"
            self.params = {}
            self.initParam()


        def initParam(self):
            self.params["paramTask.clientCode"] = ""
            self.params["paramTask.tokenCode"] = ""
            self.params["paramTask.taskTyp"] = ""
            self.params["paramTask.userCallCode"] = ""
            self.params["userCallCodePath"] = ""
            self.params["paramTask.priority"] = ""
            self.params["paramTask.robotCode"] = ""
            self.params["paramTask.podCode"] = ""
            self.params["paramTask.podDir"] = ""
            self.params["paramTask.podTyp"] = ""
            self.params["paramTask.taskCode"] = ""
            self.params["paramTask.matterArea"] = ""
            self.params["paramTask.agvModel"] = ""
            self.params["paramTask.materialLot"] = ""
            self.params["paramData.materialCode"] = ""
            self.params["paramData.materialLot"] = ""
            self.params["paramData.batchNum"] = ""
            self.params["paramData.realNum"] = ""
            self.params["paramData.planNum"] = ""
            self.params["paramData.errorInfo"] = ""
            self.params["paramData.carryPro"] = ""
            self.params["paramData.toolCode"] = ""

        def setTaskName(self, taskName):
            self.params["paramTask.taskTyp"] = taskName
            return self

        def setCallPath(self, callPath):
            self.params["userCallCodePath"] = callPath
            return self

        def setAGV(self, AGV):
            self.params["paramTask.robotCode"] = AGV
            return self

        def setPodCode(self, podCode):
            self.params["paramTask.podCode"] = podCode
            return self

        def sendJSON(self):
            destination = self.getDestination()
            response = Web_RCS.SESSION.post(destination, data=self.params)
            return response

    class TaskOrderService(Service_Interface):
        TaskStatuDict = MainTaskStatusDict

        TaskType = {
            "Multi Point Trans pod Handler" : "BJ_01",
        }

        SubTaskType = {
            "Move AGV": "S007",
            "Move back the storage rack": "G002",
            "Not put down the rack": "G003",
            "Transfer rack": "G004"
        }

        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/transTask!findListWithPages.action?bigDataFlag=true"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.taskTyp"] = "BJ_01"
            self.params["param.taskStatus"] = -1
            self.params["param.podCode"] = ""
            self.params["param.tranTaskNum"] = ""
            self.params["param.wbCode"] = ""
            self.params["param.uname"] = ""
            self.params["param.sdateTo"] = ""
            self.params["param.edateTo"] = ""
            self.params["param.dstMapCode"] = ""
            self.params["param.robotCode"] = ""
            self.params["param.groupId"] = ""
            self.params["param.showHisData"] = False
            self.params["start"] = 1
            self.params["limit"] = 10000

        def selectTaskType(self, taskType):
            self.params["param.taskTyp"] = taskType
            return self

        def selectAGV(self, agvCode):
            self.params["param.robotCode"] = agvCode
            return self

        def selectTaskID(self, taskID):
            self.params["param.tranTaskNum"] = taskID
            return self


        def selectStartTime(self, startTime):
            self.params["param.sdateTo"] = startTime
            return self

        def selectStartTime_datetime(self, year, month, day, hour, minute, second):
            selectedTime = datetime.datetime(year, month, day, hour, minute, second)
            self.params["param.sdateTo"] = selectedTime.strftime("%Y-%m-%d %H:%M:%S")
            return self

        def selectEndTime(self, endTime):
            self.params["param.edateTo"] = endTime
            return self

        def selectEndTime_datetime(self, year, month, day, hour, minute, second):
            selectedTime = datetime.datetime(year, month, day, hour, minute, second)
            self.params["param.edateTo"] = selectedTime.strftime("%Y-%m-%d %H:%M:%S")
            return self

        def selectStatus(self, status):
            self.params["param.taskStatus"] = status
            return self

        def selectLimit(self, limit):
            self.params["limit"] = limit
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data= self.params)
            return result


        # extended function
        def getAllCurrentExecutingMainTask(self):
            agvList = json.loads(Web_RCS.AGVListService().sendJSON().text)["data"]
            mainTaskIDDict = {}
            mainTaskService = Web_RCS.TaskOrderService()
            response = mainTaskService.selectAGV(",".join(agvList)).selectStatus(mainTaskService.TaskStatuDict["executing"]).sendJSON()
            dataResultList = json.loads(response.text)["data"]
            for data in dataResultList:
                if data["tranTaskNum"] not in mainTaskIDDict.keys():
                    mainTaskIDDict[data["tranTaskNum"]] = data
            return mainTaskIDDict



    class SubTaskOrderService(Service_Interface):
        SubTaskStatuDict = {"Time Out": 11,
                         "Created": 1,
                         "executing": 2,
                         "cancelled": 5,
                         "Picking": 7,
                         "Completed": 9
                         }
        TaskTypeDict = {
            "Not put down the rack": "G003",
            "Move back the storage rack": "G002",
            "Transfer rack": "G004"
        }

        def __init__(self):
            super().__init__()
            self.params = {}
            self.serviceLocation = "/web/subTask!findListWithPages.action"
            self._initParam()

        def _initParam(self):
            self.params["param.taskTyp"] = -1
            self.params["param.subTaskTyp"] = -1
            self.params["param.taskStatus"] = -1
            self.params["param.podCode"] = ""
            self.params["param.startTime"] = ""
            self.params["param.wbCode"] = ""
            self.params["param.callCode"] = ""
            self.params["param.subTaskNum"] = ""
            self.params["param.transTaskNum"] = ""
            self.params["param.endTime"] = ""
            self.params["param.dstMapCode"] = ""
            self.params["param.robotCode"] = ""
            self.params["param.groupId"] = ""
            self.params["param.showHisData"] = False
            self.params["start"] = 1
            self.params["limit"] = 100000

        def selectAGV(self, agvCode):
            self.params["param.robotCode"] = agvCode
            return self

        def selectTaskID(self, taskID):
            self.params["param.transTaskNum"] = taskID
            return self

        def selectSubTaskID(self, subTaskID):
            self.params["param.subTaskNum"] = subTaskID
            return self

        def selectTaskStatus(self, taskStatus):
            self.params["param.taskStatus"] = taskStatus
            return self

        def selectSubTaskType(self, subTaskType):
            self.params["param.subTaskTyp"] = subTaskType
            return self

        def selectStartTime(self, startTime):
            self.params["param.startTime"] = startTime
            return self

        def selectStartTime_datetime(self, year, month, day, hour, minute, second):
            selectedTime = datetime.datetime(year, month, day, hour, minute, second)
            self.params["param.startTime"] = selectedTime.strftime("%Y-%m-%d %H:%M:%S")
            return self

        def selectEndTime(self, endTime):
            self.params["param.endTime"] = endTime
            return self

        def selectEndTime_datetime(self, year, month, day, hour, minute, second):
            selectedTime = datetime.datetime(year, month, day, hour, minute, second)
            self.params["param.endTime"] = selectedTime.strftime("%Y-%m-%d %H:%M:%S")
            return self

        def setToady(self):
            start = datetime.datetime.now().replace(hour=0, minute=0, second=0)
            self.selectStartTime(start.strftime("%Y-%m-%d %H:%M:%S"))
            end = datetime.datetime.now()
            self.selectEndTime(end.strftime("%Y-%m-%d %H:%M:%S"))
            return self

        def sendJSON(self):
            loginService = Web_RCS.LoginService()
            loginService.runService()
            print(self.params)
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

        def setLimit(self, limit):
            self.params["limit"] = limit
            return self

        @staticmethod
        def parseSubTaskResponse(subTaskResponse):
            response = json.loads(subTaskResponse.text)
            if response["success"] != True:
                raise Exception("Request is not succeeded")
            taskList = response["data"]
            tempDict = TaskDict()
            for task in taskList:
                tempDict.extend({task["taskID"]: (task["endX"], task["endY"])}) # TaskInfo(task["endX"], task["endY"])
                # removedPodStatus[0: waiting_command, 1: can be sent, 2: sending, 3: successed, -1: failed, 5: re-sending]
            return tempDict



    class ShippingSpaceService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/shippingSpace!findListWithPages.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.orgCode"] = -1
            self.params["param.spaceCode"] = ""
            self.params["param.mapCode"] = -1
            self.params["param.status"] = -1
            self.params["param.indExp"] = ""
            self.params["param.type"] = ""
            self.params["param.locX"] = ""
            self.params["param.locY"] = ""
            self.params["param.spaceTexts"] = ""
            self.params["start"] = 1
            self.params["limit"] = 300

        def setOrgCode(self, orgCode):
            self.params["param.orgCode"] = orgCode
            return self

        def setMapCode(self, mapCode):
            self.params["param.mapCode"] = -1
            return self

        def setType(self, type):
            self.params["param.type"] = type
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result



    class MapDataService(Service_Interface):
        pointTypeDict = {"Parking Point": 19,
                         "Queuing Area": 12}
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/mapData!findListWithPages.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.orgCode"] = -1
            self.params["param.mapCode"] = -1
            self.params["param.mapDataCode"] = -1
            self.params["param.dataTyp"] = -2
            self.params["param.dataName"] = ""
            self.params["param.podCode"] = ""
            self.params["param.areaCode"] = ""
            self.params["start"] = 1
            self.params["limit"] = 5000

        def selectCallSign(self, callSign):
            self.params["param.dataName"] = callSign
            return self

        def selectPointType(self, pointTypeNumber):
            self.params["param.dataTyp"]= pointTypeNumber
            return self



        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class DroppingHoleService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/droppingHole!findListWithPages.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.orgCode"] = -1
            self.params["param.holeCode"] = ""
            self.params["param.mapCode"] = -1
            self.params["param.status"] = -1
            self.params["param.indExp"] = ""
            self.params["param.holeText"] = ""
            self.params["param.locX"] = ""
            self.params["param.locY"] = ""
            self.params["param.shopCodes"] = ""
            self.params["start"] = 1
            self.params["limit"] = 200

        def setOrgCode(self, orgCode):
            self.params["param.orgCode"] = orgCode
            return self

        def setMapCode(self, mapCode):
            self.params["param.mapCode"] = -1


        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class RackNumberService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/pod!findPodListWithPages.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.podCode"] = ""
            self.params["param.orgCode"] = -1
            self.params["param.podTypCode"] = -1
            self.params["param.areaTypCode"] = -1
            self.params["param.indBlk"] = -1
            self.params["param.indBlkU"] = -1
            self.params["param.berthCode"] = ""
            self.params["start"] = 1
            self.params["limit"] = 1000



        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result



    class AGVTaskStatisticsService_DayCount(Service_Interface):

        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/transTaskStatistics!findEveryDayStatListWithPages.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.mapCode"] = "XY"
            self.params["start"] = 1
            self.params["limit"] = 50

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class AGVTaskStatisticsService_HourCount(Service_Interface):

        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/transTaskStatistics!statByHour.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.mapCode"] = "XY"

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class AGVTaskStatisticsService_MinuteCount(Service_Interface):

        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/transTaskStatistics!statByMin.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.mapCode"] = "XY"

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class AGVTaskStatisticsService_CompletedTask(Service_Interface):

        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/transTaskStatistics!statSubTaskComplete.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.mapCode"] = "XY"
            self.params["param.beginDate"] = datetime.datetime.today().replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
            self.params["param.endDate"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        def selectStartTime(self, startTime):
            self.params["param.beginDate"] = startTime
            return self

        def selectEndTime(self, endTime):
            self.params["param.endDate"] = endTime
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

        def getCombinedStationResultDict(self):
            stationDict = {}
            resultDict = {}
            addedStationList = []
            response = self.sendJSON()
            dataList = json.loads(response.text)
            # turn dataList into dict
            for dataDict in dataList["obj"]:
                stationDict[dataDict["dataName"]] = dataDict["podNum"]

            for stationCallSign, podNum in stationDict.items():
                if stationCallSign in addedStationList:
                    continue
                if stationCallSign in COMBINED_STATION_DICT.keys():
                    pairedStation = COMBINED_STATION_DICT[stationCallSign]
                    combinedStation = stationCallSign + "-" + pairedStation
                    resultDict[combinedStation] = stationDict[stationCallSign] + stationDict[pairedStation]
                    addedStationList.append(stationCallSign)
                    addedStationList.append(pairedStation)
                else:
                    resultDict[stationCallSign] = stationDict[stationCallSign]
                    addedStationList.append(stationCallSign)
            return resultDict

    class AGVTaskStatisticsService_UncompletedTask(Service_Interface):

        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/transTaskStatistics!statSubTaskUncomplete.action"
            self.params = {}
            self._initParam()

        def getCombinedStationResultDict(self):
            stationDict = {}
            resultDict = {}
            addedStationList = []
            response = self.sendJSON()
            dataList = json.loads(response.text)
            # turn dataList into dict
            for dataDict in dataList["obj"]:
                stationDict[dataDict["dataName"]] = dataDict["podNum"]

            for stationCallSign, podNum in stationDict.items():
                if stationCallSign in addedStationList:
                    continue
                if stationCallSign in COMBINED_STATION_DICT.keys():
                    pairedStation = COMBINED_STATION_DICT[stationCallSign]
                    combinedStation = stationCallSign + "-" + pairedStation
                    resultDict[combinedStation] = stationDict[stationCallSign] + stationDict[pairedStation]
                    addedStationList.append(stationCallSign)
                    addedStationList.append(pairedStation)
                else:
                    resultDict[stationCallSign] = stationDict[stationCallSign]
                    addedStationList.append(stationCallSign)
            return resultDict


        def _initParam(self):
            self.params["param.mapCode"] = "XY"

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result



    class AGVListService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.mapCode = "XY"
            self.serviceLocation = "/web/device!findListWithPages.action?elcMapCode={}&code="
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["contains"] = "false"
            self.params["start"] = 1
            self.params["limit"] = 500


        def sendJSON(self):
            self.serviceLocation = self.serviceLocation.format(self.mapCode)
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class TaskSentMessageService(Service_Interface):
        StatusDict = {"Error sending" :0,
                        "Created":1,
                        "Sending": 3 ,
                        "Completed": 9}

        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/sendMsgExp!findListWithPages.action?bigDataFlag=true"
            self.params = {}
            self._initParam()


        def _initParam(self):
            self.params["param.reqCode"] = ""
            self.params["param.reqTyp"] = "/agvCallBack"
            self.params["param.sendStatus"] = -1
            self.params["param.rcptStatus"] = -1
            self.params["param.msgTyp"] = -1
            self.params["param.msgFrom"] = ""
            self.params["param.taskCode"] = ""
            self.params["param.startTimeFrom"] = ""
            self.params["param.startTimeTo"] = ""
            self.params["param.endTimeFrom"] = datetime.datetime.today().replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
            self.params["param.endTimeTo"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            self.params["param.showHisData"] = False
            self.params["param.sendMsg"] = ""
            self.params["param.method"] = ""
            self.params["start"] = 1
            self.params["limit"] = 1500

        def setRequestContent(self, content):
            self.params["param.sendMsg"] = content
            return self

        def setReqType(self, reqType):
            self.params["param.reqTyp"] = ""
            return self

        def setEndTimeFrom(self, endTimeFrom):
            self.params["param.endTimeFrom"] = endTimeFrom
            return self

        def setEndTimeTo(self, endTimeTo):
            self.params["param.endTimeTo"] = endTimeTo
            return self

        def setSendStatus(self, status):
            self.params["param.sendStatus"] = Web_RCS.TaskSentMessageService.StatusDict[status]
            return self

        def parseTaskSentMessagesendMsg(self, sendMsgText):
            sendMsgDict = json.loads(sendMsgText)
            return sendMsgDict

        def parseTaskReturnMessage(self, reqMsg):
            reqMsg = json.loads(reqMsg)
            return reqMsg

        def setLimit(self, limit):
            self.params["limit"] = limit
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result


    class ResendingErrorMessage(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/sendMsgExp!handleExceptionMsg.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.reqCode"] = "" #

        def setReqCode(self, reqCode):
            self.params["param.reqCode"] = reqCode  #

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class InterfaceCallingLogService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/interLog!findListWithPages.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.terminalTyp"] = "-1" #
            self.params["param.resultCode"] = "-1"  #
            self.params["param.interMethod"] = ""  #
            self.params["param.beginDate"] = datetime.datetime.today().replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")  #
            self.params["param.endDate"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")  #
            self.params["param.argsParam"] = ""  #
            self.params["param.showHisData"] = "false"  #
            self.params["start"] = 1
            self.params["limit"] = 500


        def setInterMethod(self, interMethod):
            self.params["param.interMethod"] = interMethod
            return self

        def setLimit(self, limit):
            self.params["limit"] = limit
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class ResendingErrorMessage(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/sendMsgExp!handleExceptionMsg.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.reqCode"] = "" #

        def setReqCode(self, reqCode):
            self.params["param.reqCode"] = reqCode  #

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class AlarmService(Service_Interface):
        MainAlarmType = {"Security Alarm":17}
        WorkingStatus = {"WhatEver": -1, "Begin": 1, "End": 2}
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/alarm!findListWithPages.action?bigDataFlag=true"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.elcMapCode"] = -1
            self.params["param.status"] = -1
            self.params["param.logLevel"] = -1
            self.params["param.alarmModule"] = -1
            self.params["param.orgCode"] = -1
            self.params["param.beginDate"] = ""
            self.params["param.endDate"] = ""
            self.params["param.mainAlarmTypeCode"] = Web_RCS.AlarmService.MainAlarmType["Security Alarm"]
            self.params["param.minorAlarmTypeCode"] = ""
            self.params["param.sourceName"] = ""
            self.params["param.showHisData"] = "false"
            self.params["start"] = 1
            self.params["limit"] = 10000
            self.params["sortName"] = "timeInterVal"
            self.params["sortOrder"] = "asc"



        def selectStartTime(self, startDateTimeStr):
            self.params["param.beginDate"] = startDateTimeStr
            return self

        def selectEndTime(self, endDataTimeStr):
            self.params["param.endDate"] = endDataTimeStr
            return self

        def selectWorkingStatus(self, workingStatus):
            self.params["param.status"] = workingStatus
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class GenAgvSchedulingTask(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/services/rest/hikRpcService/genAgvSchedulingTask"
            self.params = {}
            self._initParam()

        def _initParam(self):
            pass

        def setJson(self, targetJson):
            self.json = targetJson
            return self

        def selectStartTime(self, startDateTimeStr):
            self.params["param.beginDate"] = startDateTimeStr
            return self

        def selectEndTime(self, endDataTimeStr):
            self.params["param.endDate"] = endDataTimeStr
            return self

        def selectWorkingStatus(self, workingStatus):
            self.params["param.status"] = workingStatus
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.json)
            return result

    class GenAgvSchedulingTask(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/services/rest/hikRpcService/continueTask"
            self.params = {}
            self._initParam()

        def _initParam(self):
            pass

        def setJson(self, targetJson):
            self.json = targetJson
            return self

        def selectStartTime(self, startDateTimeStr):
            self.params["param.beginDate"] = startDateTimeStr
            return self

        def selectEndTime(self, endDataTimeStr):
            self.params["param.endDate"] = endDataTimeStr
            return self

        def selectWorkingStatus(self, workingStatus):
            self.params["param.status"] = workingStatus
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.json)
            return result

    class ShippingSpaceAllocationService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/shippingSpace!allotQueue.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.spaceCodes"] = ""
            self.params["param.queueMin"] = 3
            self.params["param.queueMax"] = 3

        def setLocation(self, location):
            self.params["param.spaceCodes"] = location
            return self

        def setMaxQueue(self, maxQueue):
            self.params["param.queueMax"] = maxQueue
            return self

        def setMinQueue(self, minQueue):
            self.params["param.queueMin"] = minQueue
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class ShippingHoleSwitchSpaceService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/shippingSpace!switchSpace.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.spaceCodes"] = ""
            self.params["param.status"] = 1 # 1 -> open, 0 -> close

        def setLocation(self, location):
            self.params["param.spaceCodes"] = location
            return self

        def setOpenClose(self, openClose):
            self.params["param.status"] = openClose
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class DroppingSpaceAllocationService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/droppingHole!allotQueue.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.holeCodes"] = ""
            self.params["param.queueMin"] = 3
            self.params["param.queueMax"] = 3

        def setLocation(self, location):
            self.params["param.holeCodes"] = location
            return self

        def setMaxQueue(self, maxQueue):
            self.params["param.queueMax"] = maxQueue
            return self

        def setMinQueue(self, minQueue):
            self.params["param.queueMin"] = minQueue
            return self


        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class DroppingSpaceSwitchService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/droppingHole!switchHole.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.holeCodes"] = ""
            self.params["param.status"] = 1

        def setLocation(self, location):
            self.params["param.holeCodes"] = location
            return self

        def setOpenClose(self, openClose):
            self.params["param.status"] = openClose
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class StagingStrategySettingServiceView(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/stagStrategy!findListWithPages.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["contains"] = "false"
            self.params["start"] = 1
            self.params["limit"] = 50

        def setLocation(self, location):
            self.params["param.holeCodes"] = location
            return self

        def setOpenClose(self, openClose):
            self.params["param.status"] = openClose
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class StagingStrategySettingServiceAdd(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/stagStrategy!save.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.id"] = ""
            self.params["param.stagStart"] = ""
            self.params["param.stagEnd"] = ""
            self.params["param.stagFree"] = ""
            self.params["param.freeInterval"] = ""
            self.params["param.type"] = "Add"


        def setId(self, id):
            self.params["param.id"] = id
            return self

        def setStart(self, stagStart):
            self.params["param.stagStart"] = stagStart
            return self

        def setEnd(self, stagEnd):
            self.params["param.stagEnd"] = stagEnd
            return self

        def setFreeTime(self, stagFree):
            self.params["param.stagFree"] = stagFree
            return self

        def setFreeInterval(self, freeInterval):
            self.params["param.freeInterval"] = freeInterval
            return self

        def setType(self, type):
            self.params["param.type"] = type
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class StagingStrategySettingServiceDelete(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/stagStrategy!delete.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.ids"] = ""
            self.params["param.type"] = "Delete"

        def setId(self, id):
            self.params["param.ids"] = id
            return self

        def setType(self, type):
            self.params["param.type"] = type
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class StagingStrategySettingServiceDeploy(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/stagStrategy!remote.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            pass

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class ResumePauseAGVService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/agvControl!stopResumeOffline.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.clientCode"] = ""
            self.params["param.robotCount"] = ""
            self.params["param.mapShortName"] = ""
            self.params["robots"] = ""
            self.params["stopResumeOffline"] = ""

        def stopAGV(self, agvNum):
            self.params["robots"] = agvNum
            self.params["stopResumeOffline"] = "stop"
            return self

        def resumeAGV(self, agvNum):
            self.params["robots"] = agvNum
            self.params["stopResumeOffline"] = "resume"
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class ExcludeAGVService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/agvControl!excludeAgv.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.clientCode"] = ""
            self.params["robotCode"] = ""

        def excludeAGV(self, agvNum):
            self.params["robotCode"] = "{},1".format(agvNum)
            return self

        def cancelExcludeAGV(self, agvNum):
            self.params["robotCode"] = "{},0".format(agvNum)
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

    class AGVStatusService(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "/web/agvControl!getAgvStatus.action"
            self.params = {}
            self._initParam()

        def _initParam(self):
            self.params["param.clientCode"] = ""
            self.params["param.robotCount"] = ""
            self.params["param.mapShortName"] = ""
            self.params["robots"] = ""

        def selectAGV(self, agvNum):
            self.params["robots"] = agvNum
            return self

        def sendJSON(self):
            result = Web_RCS.SESSION.post(self.getDestination(), data=self.params)
            return result

class RCS_SUPPORT:

    @staticmethod
    def getSystemURL():
        if RCS_CONSTANT.PROTOCOL and RCS_CONSTANT.IP and RCS_CONSTANT.SUPPORT_PORT and RCS_CONSTANT.SYSTEM:
            return "{}://{}:{}/{}".format(RCS_CONSTANT.PROTOCOL, RCS_CONSTANT.IP, RCS_CONSTANT.SUPPORT_PORT, RCS_CONSTANT.SYSTEM)

    class Service_Interface():
        def __init__(self):
            self.serviceLocation = ""
            self.params = {}

        def getServiceLocation(self):
            return self.serviceLocation

        def getDestination(self):
            return RCS_SUPPORT.getSystemURL() + self.getServiceLocation()

        def sendJSON(self):
            pass

    class SUPPORT(Service_Interface):
        def __init__(self):
            self.serviceLocation = "/support/support?robotid={robotId}"
            self.params = {}
            self.resultText = ""
            self.timeout = 5

        def setRobotId(self, robotId):
            self.params["robotId"]= robotId
            return self

        def setTimeOut(self, timeout):
            self.timeout = timeout
            return self

        def sendJSON(self):
            try:
                # print(self.getDestination().format(**self.params))
                result = httpclient.get(self.getDestination().format(**self.params), timeout=self.timeout)
            except Exception as e:
                print(str(e), self.getDestination().format(**self.params))
                return "timeout"
            if not result.status_code == 200:
                return "404" # for telegram
                raise Exception("Error {}".format(result.status_code))
            if "version" not in result.text:
                return "404" # for telegram
                raise Exception("AGV {robotId} is not online".format(**self.params))

            self.resultText = result.text
            return result

        def isExcludedAGV(self):
            if "REMOVE_MASK" in self.resultText:
                return True
            return False

        def isOfflineMask(self):
            if "OFFLINE_MASK" in self.resultText:
                return True
            return False

        def getTag(self, tag):
            return re.findall("<{}>(.*?)</{}>".format(tag, tag), self.resultText)

        def getBatteryLevel(self):
            return int(self.getTag("BatteryLevel")[0])

        def getSingalLevel(self):
            return int(self.getTag("SignalLevel")[0])

        def getAGVTargetLocation(self):
            return (int(self.getTag("x")[0]), int(self.getTag("y")[0]))

        def getCurrentLocationRCS(self):
            return ( int(self.getTag("CommandX")[0]), int(self.getTag("CommandY")[0]) )

        def getCurrentLocationAGV(self):
            if self.resultText != "404":
                return ( int( re.findall("x=\"(.*?)\"", self.resultText)[0] ), int(re.findall("y=\"(.*?)\"", self.resultText)[0]) )

        def getTaskInfo(self):
            return {"taskID": self.getTaskID(), "subTaskSeq": self.getSubTaskSeq(), "targetLocation": self.getTargetLocation()}

        def getRobotStatus(self):
            return self.getTag("RobotStatus")[-1]

        def getTaskID(self):
            return self.getTag("TaskId")[-1]

        def getTaskIDList(self):
            return self.getTag("TaskId")

        def getPodID(self):
            return self.getTag("PodId")[-1]

        def getPodIDList(self):
            return self.getTag("PodId")

        def getSubTaskSeq(self):
            return self.getTag("SubTaskId")[-1]

        def getSubTaskSeqList(self):
            return self.getTag("SubTaskId")

        def getTargetLocation(self):
            return self.getTag("target_x")[-1], self.getTag("target_y")[-1]

        def getWhetherAGVOnline(self):


            agvListService = Web_RCS.AGVListService()
            result = agvListService.sendJSON()
            robotIds = json.loads(result.text)["data"]



            agv = {}
            a = {}
            for robotId1 in robotIds:
                try:
                    robotId = robotId1["code"]
                    support = RCS_SUPPORT.SUPPORT().setRobotId(robotId)
                    result = support.sendJSON()
                    batteryLevel = support.getTag("BatteryLevel")
                    x, y = support.getCurrentLocationAGV()
                    agvArea = support._determineCoordinateArea(x, y)
                    agv[robotId] = {}
                    agv[robotId]["BatteryLevel"] = batteryLevel
                    agv[robotId]["Area"] = agvArea
                    if agvArea == "404":
                        a[robotId] = {}
                        a[robotId]["x{}y{}".format(x, y)] = agvArea

                except Exception as e:
                    print(e)

        # def getAllAGVinsideParkingArea(self):
        #     agvListService = Web_RCS.AGVListService()
        #     result = agvListService.sendJSON()
        #     robotIds = json.loads(result.text)["data"]
        #
        #     agv = {}
        #     a = {}
        #     for robotId1 in robotIds:
        #         try:
        #             robotId = robotId1["code"]
        #             support = RCS_SUPPORT.SUPPORT().setRobotId(robotId)
        #             result = support.sendJSON()
        #             x, y = support.getCurrentLocationRCS()
        #             agv[robotId] = {}
        #             agv[robotId]["BatteryLevel"] = self.batteryLevel
        #             agv[robotId]["Area"] = agvArea
        #             if agvArea == "404":
        #                 a[robotId] = {}
        #                 a[robotId]["x{}y{}".format(x, y)] = agvArea
        #
        #         except Exception as e:
        #             print(e)

        @staticmethod
        def _determineCoordinateArea(x, y):
            for areaName, coordinateRangeDict in AREA_COORDINATION_DIVIDE.items():
                division = RCS_SUPPORT.SUPPORT._determineChargingStationCoordinateArea(x, y)
                if division:
                    return division
                if x >= coordinateRangeDict["x_0"] and x <= coordinateRangeDict["x_1"] and y >= coordinateRangeDict["y_0"] and y <= coordinateRangeDict["y_1"]:
                    return areaName
            return "404"

        @staticmethod
        def _determineChargingStationCoordinateArea(x, y):
            for areaName, coordinateRangeDict in CHARGING_STATION_COORDINATION.items():
                if x >= coordinateRangeDict["x_0"] and x <= coordinateRangeDict["x_1"] and y >= coordinateRangeDict["y_0"] and y <= coordinateRangeDict["y_1"]:
                    return areaName
            return ""


    class GetQueueStatus(Service_Interface):
        def __init__(self):
            super().__init__()
            self.serviceLocation = "rcs/queue/support?pointpos={x}+{y}"
            self.params = {}
            self.resultText = ""
            self.droppingSpaceStation = {}
            self.allStationQueueStatus = {}
            self._getStationMapping()

        def _getStationMapping(self):
            droppingHoleService = Web_RCS.DroppingHoleService()
            self.droppingSpaceStation = json.loads(droppingHoleService.sendJSON().text)["data"]
            # self.shippSpaceMapping
            return self


        def setCoordination(self, x, y):
            self.params["x"]= x
            self.params["y"] = y
            return self

        def setWorkingStation(self, stationCallSign):
            self.params["x"], self.params["y"] = self._stationCallSignToCoordination(stationCallSign)
            return self

        def _stationCallSignToCoordination(self, stationCallSign):
            for station in self.droppingSpaceStation:
                if stationCallSign == station["holeText"]:
                    return station["cooX"], station["cooY"]
            raise Exception("Station not found")

        def sendJSON(self):
            result = httpclient.get(self.getDestination().format(**self.params))
            if not result.status_code == 200:
                raise Exception("Error {}".format(result.status_code))
            if "version" not in result.text:
                raise Exception("Station {x}, {y} not found".format(**self.params))

            self.resultText = result.text
            return self

        def getTag(self, tag):
            return re.findall("<{}>(.*?)</{}>".format(tag, tag), self.resultText)

        def getMaxQueueNumber(self):
            return self.getTag("len")[0]

        def getQueueNumber(self):
            return self.getTag("queue")[0]

        def getWaitingAGV(self):
            return self.getTag("Robot")

        def getAllStationQueue(self):
            for station in self.droppingSpaceStation:
                if station["holeText"] not in self.allStationQueueStatus.keys():
                    self.allStationQueueStatus[station["holeText"]] = {}
                self.allStationQueueStatus[station["holeText"]]["waitingList"] = self.setCoordination(station["cooX"], station["cooY"]).sendJSON().getWaitingAGV()
                self.allStationQueueStatus[station["holeText"]]["queueNumber"] = int(self.getQueueNumber())
                self.allStationQueueStatus[station["holeText"]]["maxQueueNumber"] = int(station["queueMax"])
            return self.allStationQueueStatus

        def getNotFullQueueStation(self):
            text = ""
            for stationCallSign, stationDict in self.allStationQueueStatus.items():
                if stationDict["queueNumber"] != stationDict["maxQueueNumber"] :
                    text += "{}: {} - {}/{}\n".format(stationCallSign, stationDict["waitingList"], stationDict["queueNumber"], stationDict["maxQueueNumber"])
            return text

        def checkWhetherAGVExecutingTask(self, agvCallCode):
            if not self.allStationQueueStatus:
                raise Exception("Please update all Station Queue Status First")
            for station, stationData in self.allStationQueueStatus.items():
                if agvCallCode in stationData["waitingList"]:
                    return True
            return False


    class AGVStatusImpl(SUPPORT):
        STATUS_LIST = ["No Task", "Start to Get Pod", "Moving with Rack to station", "Queue at station",
                       "Parking", "Picking", "Charging", "Changing Battery", "Error", "Offline", "Goods unrecongized"]

        AGVDICT_KEY = ["AGV Complete Msg",
                       "AGV Status Msg",
                       "Route Planning Msg"]

        def __init__(self):
            super().__init__()
            self.queueLocationList = []


        def updateQueuegMap(self):
            if not self.queueLocationList:
                self._getQueueListFromRCS()
            return self

        def _getAGVSubTaskDataFromRCS(self):
            subTaskService = Web_RCS.SubTaskOrderService()
            subTaskService.selectSubTaskType(subTaskService.SubTaskStatuDict["executing"])
            response = subTaskService.sendJSON()
            executingDataList = json.loads(response.text)["data"]

            subTaskService.selectSubTaskType(subTaskService.SubTaskStatuDict["Picking"])
            response = subTaskService.sendJSON()
            pickingDataList = json.loads(response.text)["data"]

            dataList = executingDataList + pickingDataList



        def _getQueueListFromRCS(self):
            mapService = Web_RCS.MapDataService()
            mapService.selectPointType(Web_RCS.MapDataService.pointTypeDict["Queuing Area"])
            response = mapService.sendJSON()
            mapDataList = json.loads(response.text)["data"]
            for data in mapDataList:
                self.queueLocationList.append((data["cooX"], data["cooY"]))
            return self


        def getInfoToDetermineAGVStatus(self):




            podIDList = self.getPodIDList()
            taskIDList = self.getTaskIDList()
            subTaskSeqList = self.getSubTaskSeqList()

            agvDict = {"AGV Complete Msg": {},
                       "AGV Status Msg": {},
                       "Route Planning Msg": {}}

            agvDict["AGV Status Msg"]["robotStatus"] = self.getRobotStatus()
            agvDict["AGV Complete Msg"]["agvCurrentLocation"] = self.getCurrentLocationAGV()


            agvDict["AGV Complete Msg"]["taskID"] = taskIDList[0]
            agvDict["AGV Status Msg"]["taskID"] = taskIDList[1]
            agvDict["Route Planning Msg"]["taskID"] = taskIDList[2]

            agvDict["AGV Complete Msg"]["subTaskID"] = subTaskSeqList[0]
            agvDict["AGV Status Msg"]["subTaskID"] = subTaskSeqList[1]
            agvDict["Route Planning Msg"]["subTaskID"] = subTaskSeqList[2]

            agvDict["AGV Complete Msg"]["podID"] = podIDList[0]
            agvDict["AGV Status Msg"]["podID"] = podIDList[1]




            return agvDict

        def _deterAGVNoTask(self, agvMsgDict):
            # all 3 taskID == 0 and all 2 rackID ==0 -->   not all 3 taskID == 0 or not all 2 rackID !=0
            agvDictKeyFull = RCS_SUPPORT.AGVStatusImpl.AGVDICT_KEY
            agvDictKey = agvDictKeyFull[:2]

            for key in agvDictKey:
                if agvMsgDict[key]["taskID"] != "0" or agvMsgDict[key]["podID"] != "0":
                    return False
            if agvMsgDict[agvDictKeyFull[2]]["taskID"] != "0":
                return False

            return True

        def _determineAGVStartGetPod(self, agvMsgDict):
            # all 3 SubTaskID == 0 and all 2 rackID ==0
            agvDictKeyFull = RCS_SUPPORT.AGVStatusImpl.AGVDICT_KEY
            agvDictKey = agvDictKeyFull[0:1]

            for key in agvDictKey:
                if agvMsgDict[key]["subTaskID"] != "0" or agvMsgDict[key]["podID"] != "0" or agvMsgDict[key]["taskID"] == "0":
                    return False
            if agvMsgDict[agvDictKeyFull[2]]["subTaskID"] != "0":
                return False

            return True

        def _determineAGVMovingToStation(self, agvMsgDict):
            # all SubTaskID equal and != 0 , 1 RobotStatus == 2

            agvMsgDictKeyList = list(agvMsgDict.keys())
            for i in range(len(agvMsgDictKeyList) - 1):
                agvMsgDictKeyA = agvMsgDictKeyList[i]
                agvMsgDictKeyB = agvMsgDictKeyList[i + 1]
                if agvMsgDict[agvMsgDictKeyA]["subTaskID"] == "0" or agvMsgDict[agvMsgDictKeyB]["subTaskID"] == "0":
                    return False
                if agvMsgDict[agvMsgDictKeyA]["subTaskID"] != agvMsgDict[agvMsgDictKeyB]["subTaskID"]:
                    return False

            if not self.queueLocationList:
                raise Exception("Please update queueLocationList from RCS first")

            for queuePoint in self.queueLocationList:
                xCoordination, yCoordination = agvMsgDict["AGV Complete Msg"]["agvCurrentLocation"][0], \
                                               agvMsgDict["AGV Complete Msg"]["agvCurrentLocation"][1]
                if withInRange(xCoordination, queuePoint[0] - 600, queuePoint[0] + 600) and \
                        withInRange(yCoordination, queuePoint[1] - 600, queuePoint[1] + 600):
                    return False

            return True

        def _determineAGVQueueAtStation(self, agvMsgDict):
            # all SubTaskID equal and != 0 , 1 RobotStatus == 4

            agvMsgDictKeyList = list(agvMsgDict.keys())
            for i in range(len(agvMsgDictKeyList) - 1):
                agvMsgDictKeyA = agvMsgDictKeyList[i]
                agvMsgDictKeyB = agvMsgDictKeyList[i + 1]
                if agvMsgDict[agvMsgDictKeyA]["subTaskID"] == "0" or agvMsgDict[agvMsgDictKeyB]["subTaskID"] == "0":
                    return False
                if agvMsgDict[agvMsgDictKeyA]["subTaskID"] != agvMsgDict[agvMsgDictKeyB]["subTaskID"]:
                    return False

            if not self.queueLocationList:
                raise Exception("Please update queueLocationList from RCS first")

            for queuePoint in self.queueLocationList:
                xCoordination, yCoordination = agvMsgDict["AGV Complete Msg"]["agvCurrentLocation"][0], agvMsgDict["AGV Complete Msg"]["agvCurrentLocation"][1]
                if withInRange(xCoordination, queuePoint[0] - 600, queuePoint[0] + 600) and\
                        withInRange(yCoordination, queuePoint[1] - 600, queuePoint[1] + 600):
                    return True

            return False

        def determineAGVQueueAtStation(self, agvMsgDict):
            return self._determineAGVQueueAtStation(agvMsgDict)

        def _determineAGVAtParking(self, agvMsgDict):
            # all 3 TaskID == 0 and 2 rackID != 0 and agv stop
            agvDictKeyFull = RCS_SUPPORT.AGVStatusImpl.AGVDICT_KEY
            agvDictKey = agvDictKeyFull[0:1]

            for key in agvDictKey:
                if agvMsgDict[key]["taskID"] != "0" or agvMsgDict[key]["podID"] == "0":
                    return False
            # if agvMsgDict[agvDictKeyFull[2]]["taskID"] != "0":
            #     return False

            if agvMsgDict["AGV Status Msg"]["robotStatus"] != "4": # agv stop status
                return False

            return True

        def _determineAGVAtPicking(self, agvMsgDict):
            if agvMsgDict["AGV Complete Msg"]["agvCurrentLocation"] == (-888, -888):
                return True
            return False

        def _determineAGVCharging(self, agvMsgDict):
            if agvMsgDict["AGV Status Msg"]["robotStatus"] == "7":
                return True
            return False

        def _determineAGVChangingBattery(self, agvMsgDict):
            if agvMsgDict["AGV Status Msg"]["robotStatus"] == "251":
                return True
            return False

        def _determineAGVError(self, agvMsgDict):
            if agvMsgDict["AGV Status Msg"]["robotStatus"] == "81":
                return True
            return False

        def _determineAGVRearBump(self, agvMsgDict):
            if agvMsgDict["AGV Status Msg"]["robotStatus"] == "3":
                return True
            return False

        def _determineAGVRotation(self, agvMsgDict):
            if agvMsgDict["AGV Status Msg"]["robotStatus"] == "1":
                return True
            return False

        def _determineGoodsUnRecognize(self, agvMsgDict):
            if agvMsgDict["AGV Status Msg"]["robotStatus"] == "11":
                return True
            return False

        def determineAGVStatus(self, agvMsgDict):
            STATUS_LIST = ["No Task", "Start to Get Pod", "Moving with Rack to station", "Queue at station",
                           "Parking", "Picking", "Charging", "Changing Battery", "Error", "Offline", "Goods unrecongized"]

            # Supporrt
            if self._determineAGVAtPicking(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[5]
            if self._determineAGVChangingBattery(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[7]
            if self._determineAGVQueueAtStation(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[3]
            if self._determineAGVAtParking(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[4]

            # Web RCS
            if self._determineAGVStartGetPod(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[1]
            if self._determineAGVMovingToStation(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[2]
            if self._deterAGVNoTask(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[0]



            # Left
            if self._determineAGVCharging(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[6]
            if self._determineAGVError(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[8]
            if self._determineAGVRearBump(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[9]
            if self._determineGoodsUnRecognize(agvMsgDict):
                return RCS_SUPPORT.AGVStatusImpl.STATUS_LIST[10]



def getAGVUnArrivedPointList(agvList):
    mainTaskIDDict = {}
    agvDict = {}
    mainTaskService = Web_RCS.TaskOrderService()
    response = mainTaskService.selectAGV(",".join(agvList)).selectStatus(mainTaskService.TaskStatuDict["executing"]).sendJSON()
    dataResultList = json.loads(response.text)["data"]
    for data in dataResultList:
        agvDict[data["robotCode"]] = data
        if data["tranTaskNum"] not in mainTaskIDDict.keys():
            mainTaskIDDict[data["tranTaskNum"]] = data

    subTaskService = Web_RCS.SubTaskOrderService()
    subTaskResponse = subTaskService.selectTaskID(",".join(mainTaskIDDict.keys())).sendJSON()
    subTaskDataResultList = json.loads(subTaskResponse.text)["data"]

    subTaskSeqDict = {}
    subTaskLastExecutingSeqDict = {}
    agvLeftPoint = {}
    for data in subTaskDataResultList:
        if data["tranTaskNum"] not in subTaskSeqDict.keys():
            subTaskSeqDict[data["tranTaskNum"]] = {}
        if data["tranTaskNum"] not in subTaskLastExecutingSeqDict.keys():
            subTaskLastExecutingSeqDict[data["tranTaskNum"]] = {}

        subTaskSeqDict[data["tranTaskNum"]][data["subTaskSeq"]] = data
        if data["taskStatus"] == str(subTaskService.SubTaskStatuDict["executing"]) or  str(data["taskStatus"] == subTaskService.SubTaskStatuDict["Picking"]):
            subTaskLastExecutingSeqDict[data["tranTaskNum"]] = data

    for taskID, subTaskData in subTaskSeqDict.items():
        arrivedPoint = []
        agvCode = subTaskData[subTaskLastExecutingSeqDict[taskID]["subTaskSeq"]]["robotCode"][0:4]
        if agvCode not in agvLeftPoint.keys():
            agvLeftPoint[agvCode] = {}
            agvLeftPoint[agvCode]["leftViaPoint"] = []
        taskViaPointList = list(mainTaskIDDict[taskID]["via"].replace("[", "").replace("]", "").replace("\"", "").split(","))
        for seqNum, subTask in subTaskData.items():
            if subTask["taskStatusStr"] != "Created" and subTask["startDataName"] in taskViaPointList:
                arrivedPoint.append(subTask["startDataName"])
                taskViaPointList.remove(subTask["startDataName"])
        agvLeftPoint[agvCode]["leftViaPoint"] = taskViaPointList
        agvLeftPoint[agvCode]["taskID"] = taskID
        agvLeftPoint[agvCode]["arrivedPoint"] = arrivedPoint
    return agvLeftPoint





if __name__ == "__main__":

    rcs = Web_RCS().addServie(Web_RCS.LoginService())
    loginService = rcs.getService("LoginService")
    loginService.runService()

    # rcs = Web_RCS().addServie(Web_RCS.TaskDispatchService())
    # # rcs.setCookiesHIKCOOKIES("16EE90FD0921MEQ").setCookiesJSESSION("81CBCB3E403C38D68EAF2D55C54E9D4F")
    # taskService = rcs.getService("TaskDispatchService")\
    #                 .setTaskName("MOVE3_HC").setCallPath("W227").setAGV("7018")
    # result = taskService.sendJSON()
    #
    rcs.addServie(Web_RCS.TaskOrderService())
    taskOrderService = rcs.getService("TaskOrderService").selectStatus(rcs.TaskOrderService.TaskStatuDict["Completed"])
    result = taskOrderService.sendJSON()
    a = json.loads(result.text)

    # rcs.addServie(Web_RCS.SubTaskOrderService())
    # subTaskOrderService = rcs.getService("SubTaskOrderService").selectTaskID("")
    # result = subTaskOrderService.sendJSON()
    # b = json.loads(result.text)
    #





    # rcs.addServie(Web_RCS.ShippingSpaceService())
    # shippingSpaceService = rcs.getService("ShippingSpaceService")
    # result = shippingSpaceService.sendJSON()
    # c = json.loads(result.text)
    #
    # rcs.addServie(Web_RCS.MapDataService())
    # mapDataService = rcs.getService("MapDataService")
    # location_jsonResult = mapDataService.sendJSON()
    # d = json.loads(location_jsonResult.text)
    #
    # rcs.addServie(Web_RCS.DroppingHoleService())
    # droppingHolesService = rcs.getService("DroppingHoleService")
    # location_jsonResult = droppingHolesService.sendJSON()
    # d = json.loads(location_jsonResult.text)
    #
    # dayCountService = json.loads(Web_RCS.AGVTaskStatisticsService_DayCount().sendJSON().text)
    # hourCountService = json.loads(Web_RCS.AGVTaskStatisticsService_HourCount().sendJSON().text)
    # completedTaskService = json.loads(Web_RCS.AGVTaskStatisticsService_CompletedTask().sendJSON().text)
    # unCompletedTaskService = json.loads(Web_RCS.AGVTaskStatisticsService_UncompletedTask().sendJSON().text)

    # agvListService = Web_RCS.AGVListService()
    # result = agvListService.sendJSON()
    # robotIds = json.loads(result.text)["data"]
    #
    # agv = {}
    # a = {}
    # for robotId1 in robotIds:
    #     try:
    #         robotId = robotId1["code"]
    #         support = RCS_SUPPORT.SUPPORT().setRobotId(robotId)
    #         result = support.sendJSON()
    #         batteryLevel = support.getTag("BatteryLevel")
    #         x, y = support.getCurrentLocationRCS()
    #         agvArea = support._determineCoordinateArea(x, y)
    #         agv[robotId] = {}
    #         agv[robotId]["BatteryLevel"] = batteryLevel
    #         agv[robotId]["Area"] = agvArea
    #         if agvArea == "404":
    #             a[robotId] = {}
    #             a[robotId]["x{}y{}".format(x, y)] = agvArea
    #
    #     except Exception as e:
    #         print(e)
    #
    # a = {}
    # b = {}
    # for value in d["data"]:
    #     location = support._determineCoordinateArea(value["cooX"], value["cooY"])
    #     a["x{}y{}".format(value["cooX"], value["cooY"])] = location
    #     if location == "Charging_Station_Left_1":
    #         b["x{}y{}".format(value["cooX"], value["cooY"])] = location



    # getQueue = RCS_SUPPORT.getQueueStatus()
    # text = getQueue.setWorkingStation("A131").sendJSON()
    # print(getQueue.getMaxQueueNumber(), getQueue.getQueueNumber(), getQueue.getWaitingAGV())
    # waitingAGV = getQueue.getWaitingAGV()
    # stationQueue = getQueue.getAllStationQueue()
    # print(getQueue.getNotFullQueueStation())

    # errorSendingStatus = {"404":{}, "500":{}}
    #     # sentMessageServie = Web_RCS.TaskSentMessageService()
    #     # response = sentMessageServie.setSendStatus("Error sending").sendJSON()
    #     # result = json.loads(response.text)
    #     # resultDataList = result["data"]
    #     # subTaskCheckTaskID = []
    #     # a = ""
    #     # for task in resultDataList:
    #     #     task["sendMsg"] = json.loads(task["sendMsg"])
    #     #     a += (task["taskCode"] + ",")
    #     #
    #     # subTaskOrderService = Web_RCS.SubTaskOrderService()
    #     # rcs.addServie(Web_RCS.SubTaskOrderService())
    #     # subTaskOrderService = subTaskOrderService.selectSubTaskID(a).setLimit(100)
    #     # result = subTaskOrderService.sendJSON()
    #     # subTaskIDList = json.loads(result.text)["data"]
    #     #
    #     # subTaskStatus = {}
    #     # for task in subTaskIDList:
    #     #     # if "Completed" == task["taskStatusStr"]:
    #     #     #     continue
    #     #     if task["taskStatusStr"] not in subTaskStatus.keys():
    #     #         subTaskStatus[task["taskStatusStr"]] = []
    #     #     subTaskStatus[task["taskStatusStr"]].append(task["subTaskNum"])

    # loginService = rcs.getLoginService()  # login
    # result = loginService.runService()
    # taskOrderService = Web_RCS.TaskOrderService()

    today = datetime.datetime.today()
    currentTime = (today - datetime.timedelta(days= 1)).replace(hour= 0, minute=0, second= 0)
    endTime = currentTime + datetime.timedelta(days=2)
    currentTimeStr = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    endTimeStr = endTime.strftime("%Y-%m-%d %H:%M:%S")
    # currentTimeMinus = (today - datetime.timedelta(minutes= 60)).strftime("%Y-%m-%d %H:%M:%S")
    response = taskOrderService.selectEndTime(endTimeStr).selectStartTime(currentTimeStr) \
        .sendJSON()
    result = json.loads(response.text)
    resultDataList = result["data"]

    # for task in resultDataList:
    #     task["sendMsg"] = json.loads(task["sendMsg"])
    #
    # msg = ""
    # if resultDataList:
    #     for data in resultDataList:
    #         msg += "Status: {sendStatusStr}\nDate Created: {dateCr}\nSend Message: {sendMsg}\n Response Msg:{reqMsg}\n\n".format(**data)
    #
    # print(msg)


    startTime = currentTime
    timeIntervalList = [startTime]
    while startTime <= endTime:
        startTime += datetime.timedelta(minutes=1)
        timeIntervalList.append(startTime)

    hourCountDict = {}

    for i in range(len(timeIntervalList) - 1):
        timeIntervalStr = timeIntervalList[i].strftime("%Y-%m-%d %H:%M:%S") + " to " + timeIntervalList[i + 1].strftime("%Y-%m-%d %H:%M:%S")
        hourCountDict[timeIntervalStr] = 0

    for task in resultDataList:

        dateCr = datetime.datetime.strptime(task["dateCr"], "%Y-%m-%d %H:%M:%S")
        dateChg = datetime.datetime.strptime(task["dateChg"], "%Y-%m-%d %H:%M:%S")
        if task["taskStatusStr"] == ' executing ':
            timeafterCreated = 0
            for i in range(len(timeIntervalList) ):
                if dateCr >= timeIntervalList[i]:
                    timeafterCreated = i
            if timeafterCreated == 0:
                break
            for j in range(timeafterCreated, len(timeIntervalList) - 1):
                if timeIntervalList[j + 1] >= datetime.datetime.now():
                    break
                timeIntervalStr = timeIntervalList[j].strftime("%Y-%m-%d %H:%M:%S") + " to " + timeIntervalList[j + 1].strftime("%Y-%m-%d %H:%M:%S")
                hourCountDict[timeIntervalStr] += 1

        if task["taskStatusStr"] == "Completed": # still need to be configured
            for i in range(len(timeIntervalList) - 1):
                if  not (timeIntervalList[i+1] < dateCr or timeIntervalList[i] > dateChg):
                    timeIntervalStr = timeIntervalList[i].strftime("%Y-%m-%d %H:%M:%S") + " to " + timeIntervalList[i + 1].strftime("%Y-%m-%d %H:%M:%S")
                    hourCountDict[timeIntervalStr] += 1

    with open("result3.txt", "w+") as file:
        text = ""
        #
        # sum = 0
        # count = 0
        for time, values in hourCountDict.items():
            # average = 0
            # sum += values
            # count += 1
            # if count > 30:
            #     sumTime =
            text += "{}: {}\n".format(time, values)
        file.write(text)



    ## Get AGV uncompleted uncompleted destination
    # result = getAGVUnArrivedPointList(["7005", "7089"])
    # getQueue = RCS_SUPPORT.getQueueStatus()
    # for agvCode, agvValues in result.items():
    #     for station in agvValues["leftViaPoint"]:
    #         text = getQueue.setWorkingStation(station).sendJSON()
    #         print(agvCode, station, getQueue.getMaxQueueNumber(), getQueue.getQueueNumber(), getQueue.getWaitingAGV())

# waitingAGV = getQueue.getWaitingAGV()
# stationQueue = getQueue.getAllStationQueue()
# print(getQueue.getNotFullQueueStation())
