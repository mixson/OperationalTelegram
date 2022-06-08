import datetime, time

import os, sys
import logging
import pickle
import ast
import json
import traceback

currentDir = "\\".join(os.getcwd().split("\\")[0:-1])
sys.path.insert(0, currentDir)

from src.telegramBot import editsStagingMorning, editsStagingNight, getMorningStagingTime, getNightStagingTime
from src.telegramBot import editBound, updateQueueSetToRCS, getQueueSetFromPickle

from values.RCS_CONSTANT import ROUTE_FILENAME_DICT

from utils.Web_Rcs import Web_RCS
# from utils import RCS_Statistics
from values import RCS_CONSTANT

loggingDirPath = os.path.join(currentDir, "log")

SLEEP_TIME = 30

def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = getLogger()
            tb = traceback.format_exc()
            logger.error(tb)
            logger.error(str(e))
    return inner_function

def logUserRecord(func):
    def inner_function(*args, **kwargs):

        logger = getLogger()
        bot = args[0]
        update = args[1]
        # userInfoLog = str(update.effective_message.chat)
        fullName = update.message.from_user.full_name
        userId = update.message.from_user.id
        messageText = update.message.text

        loggingMsg = "[{} {}] Msg: {}".format(userId, fullName, messageText)
        logger.info(loggingMsg)
        return func(*args, **kwargs)
    return inner_function

def withInRange(data, start, end):
    if data >= start and data <= end:
        return True
    return False

# check staging time (morning or night)
def isNightStaging(timeDict):
    if int(timeDict["start"]) >= 1200 and int(timeDict["start"]) < 2400:
        return True
    return False

def getLogger():

    today = datetime.datetime.now()
    todayStr = "{}_{}_{}".format(today.year, today.month, today.day)
    fileName = "{}_{}.txt".format("DailyRouteLog", "{}".format(todayStr))
    # config
    logging.captureWarnings(True)
    formatter = logging.Formatter('[%(asctime)s] (%(levelname)s) %(message)s')
    myLogger = logging.getLogger("py.warnings")
    myLogger.setLevel(logging.INFO)

    if not os.path.exists(loggingDirPath):
        os.makedirs(loggingDirPath)

    if str(os.path.join(loggingDirPath, fileName)) in [handler.baseFilename for handler in myLogger.handlers if hasattr(handler, "baseFilename")]:
        logger.handlers = []

    fileHandler = logging.FileHandler(os.path.join(loggingDirPath, fileName))
    fileHandler.setFormatter(formatter)
    myLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    myLogger.addHandler(consoleHandler)

    return myLogger

def logError(msg):
    logger = getLogger()
    tb = traceback.format_exc()
    logger.error(tb)
    logger.error(str(msg))


def getStagingDictFromPickle(fileName):
    if os.path.exists(fileName) and os.path.getsize(fileName) > 0:
        with open(fileName, "rb") as file:
            a = pickle.load(file)
            print(a)
        return a
    return None

def getStagingNumMonitorDictFromPickle(fileName):
    if os.path.exists(fileName) and os.path.getsize(fileName) > 0:
        with open(fileName, "rb") as file:
            a = pickle.load(file)
            print(a)
        return a
    return dict()

def saveStagingNumMonitorDictFromPickle(data, fileName):
    with open(fileName, "wb") as file:
        pickle.dump(data, file)
    print("{} is saved".format(str(data)))

def getDictFromPickle(fileName):
    if os.path.exists(fileName) and os.path.getsize(fileName) > 0:
        with open(fileName, "rb") as file:
            a = pickle.load(file)
            print(a)
        return a
    return None

# from CONSTANT Setting
regularRouteList = list(ROUTE_FILENAME_DICT.keys())

functionDict = {key: None for key in ROUTE_FILENAME_DICT.keys()}
functionTimeDict = {key: None for key in ROUTE_FILENAME_DICT.keys()}

def readFunctionPickleData(functionName):
    pickleFileName = "{}.pkl".format(functionName)
    data = getDictFromPickle(pickleFileName)
    return data


@exception_handler
def RF_dailyStaging_Old(*args):
    autoStatingTimeList = args[0]
    now = datetime.datetime.now()
    for timeRangeDict in autoStatingTimeList:
        isNight = isNightStaging(timeRangeDict)

        if isNight:
            editsStaging = editsStagingNight
            getStagingTime = getNightStagingTime
        else:
            editsStaging = editsStagingMorning
            getStagingTime = getMorningStagingTime

        startTime = str((timeRangeDict["start"]))
        startMinute = int(startTime[-2:])
        startHour = int(startTime[:-2])
        startDateTime = now.replace(hour=startHour, minute=startMinute, second=0)

        startCheckTime = startTime
        startEditTime = startCheckTime

        endTime = str((timeRangeDict["end"]))
        endMinute = int(endTime[-2:])
        endHour = int(endTime[:-2])
        endDateTime = now.replace(hour=endHour, minute=endMinute, second=0)

        endCheckTime = endTime
        endEditTime = str(int(endCheckTime) + 100)

        print(startTime, endTime)

        txtStagingTime = getStagingTime()

        # open Staging
        if withInRange(now, startDateTime, endDateTime):
            if txtStagingTime["start"] != startEditTime and txtStagingTime["end"] != endEditTime:

                logger = getLogger()
                logger.info(
                    "RF_dailyStaging: {},  setting: {} to {}".format("Open Staging", startDateTime, endDateTime))
                editsStaging([startEditTime, endEditTime])
                print("{} - {} edit start".format(startTime, endTime))

        # close Staging
        if not withInRange(now, startDateTime, endDateTime):
            if txtStagingTime["start"] == startEditTime and txtStagingTime["end"] == endEditTime:

                logger = getLogger()
                logger.info(
                    "RF_dailyStaging: {},  setting: {} to {}".format("Close Staging", startDateTime, endDateTime))
                editsStaging([-1, -1])
                print("{} - {} edit cancel".format(startTime, endTime))

                # adding staging Queue Inspection
                idDateTimeStr = "{}to{}".format(startDateTime.strftime("%Y-%m-%d %H:%M:%S"), endDateTime.strftime("%Y-%m-%d %H:%M:%S"))
                startId = "{}_{}".format(idDateTimeStr, "0")
                endId = "{}_{}".format(idDateTimeStr, "1")

                # addStagingNumMonitor(startId, "midnight", 10)
                # addStagingNumMonitor(endId, "default", 0)


    print("--------------" * 10)

@exception_handler
def RF_dailyStaging(*args):
    autoStatingTimeList = args[0]
    now = datetime.datetime.now()
    for timeRangeDict in autoStatingTimeList:
        isNight = isNightStaging(timeRangeDict)

        if isNight:
            editsStaging = editsStagingNight
            getStagingTime = getNightStagingTime
        else:
            editsStaging = editsStagingMorning
            getStagingTime = getMorningStagingTime

        startTime = str((timeRangeDict["start"]))
        startMinute = int(startTime[-2:])
        startHour = int(startTime[:-2])
        startDateTime = now.replace(hour=startHour, minute=startMinute, second=0)

        startCheckTime = startTime
        startEditTime = startCheckTime

        endTime = str((timeRangeDict["end"]))
        endMinute = int(endTime[-2:])
        endHour = int(endTime[:-2])
        endDateTime = now.replace(hour=endHour, minute=endMinute, second=0)

        endCheckTime = endTime
        endEditTime = str(int(endCheckTime) + 100)

        print(startTime, endTime)

        stepBystep = False
        if "stepBystep" in timeRangeDict.keys() and timeRangeDict["stepBystep"]:
            stepBystep = True

        txtStagingTime = getStagingTime()

        # open Staging
        if withInRange(now, startDateTime, endDateTime):
            if txtStagingTime["start"] != startEditTime and txtStagingTime["end"] != endEditTime:

                logger = getLogger()
                logger.info(
                    "RF_dailyStaging: {},  setting: {} to {}".format("Open Staging", startDateTime, endDateTime))
                editsStaging([startEditTime, endEditTime])
                print("{} - {} edit start".format(startTime, endTime))

        # close Staging
        if not withInRange(now, startDateTime, endDateTime):

            if txtStagingTime["start"] == startEditTime and txtStagingTime["end"] == endEditTime:
                logger = getLogger()
                logger.info(
                    "RF_dailyStaging: {},  setting: {} to {} , step By step ({})".format("Close Staging", startDateTime, endDateTime, stepBystep))

                if startEditTime == "-1" and endEditTime == "-1": # exceptional case
                    continue


                #Main Edit
                if stepBystep:
                    editsStaging([startCheckTime, endCheckTime])
                else:
                    editsStaging([-1, -1])
                print("{} - {} edit cancel".format(startTime, endTime))

                # adding staging Queue Inspection
                # idDateTimeStr = "{}to{}".format(startDateTime.strftime("%Y-%m-%d %H:%M:%S"), endDateTime.strftime("%Y-%m-%d %H:%M:%S"))
                # startId = "{}_{}".format(idDateTimeStr, "0")
                # endId = "{}_{}".format(idDateTimeStr, "1")

                # addStagingNumMonitor(startId, "midnight", 10)
                # addStagingNumMonitor(endId, "default", 0)


    print("--------------" * 10)

def loginRCS():
    rcs = Web_RCS()
    loginService = rcs.getLoginService()
    loginService.runService()



def increaseQueueNumber():
    loginRCS()
    msg = ""
    queueRuleDict = RCS_CONSTANT.QUEUE_RULE_DICT
    increaseNumberDict = RCS_CONSTANT.QUEUE_INCREASE_NUMBER_DICT
    for area, rules in queueRuleDict.items():
        msg += editBound(increaseNumberDict[area], rules)
    print(msg)
    return msg

def resumeQueueNumber():
    loginRCS()
    msg = ""
    queueRuleDict = RCS_CONSTANT.QUEUE_RULE_DICT
    resumeNumberDict = RCS_CONSTANT.QUEUE_RESUME_NUMBER_DICT
    for area, rules in queueRuleDict.items():
        msg += editBound(resumeNumberDict[area], rules)
    print(msg)
    return msg

def getFileFunctionName(filename):
    print(filename)
    with open(filename) as file:
        node = ast.parse(file.read())
    classes = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    return classes

def getFunction(functionName):
    functionName = "RF_" + functionName
    current_module = sys.modules[__name__]

    allFunctionName = getFileFunctionName(__file__)
    for function in allFunctionName:
        if functionName == function.name:
            return getattr(current_module, functionName)

@exception_handler
def RF_queueNumberKeep(*args):
    autoStatingTimeList = args[0]
    now = datetime.datetime.now()
    for timeRangeDict in autoStatingTimeList:


        startTime = str(int(timeRangeDict["start"]))
        startMinute = int(startTime[-2:])
        startHour = int(startTime[:-2])
        startDateTime = now.replace(hour=startHour, minute=startMinute, second=0)

        startCheckTime = startTime
        startEditTime = startCheckTime

        endTime = str(int(timeRangeDict["end"]))
        endMinute = int(endTime[-2:])
        endHour = int(endTime[:-2])
        endDateTime = now.replace(hour=endHour, minute=endMinute, second=0)

        endCheckTime = endTime
        endEditTime = endCheckTime

        print(startTime, endTime)


        # Increase Queue
        if withInRange(now, startDateTime, startDateTime + datetime.timedelta(minutes=2)):
            logger = getLogger()
            logger.info("RF_queueNumberKeep: {},  setting: {} to {}".format("Increase Queue", startDateTime, endDateTime))
            msg = increaseQueueNumber()

            print(msg)

        # resume Queue
        if withInRange(now, endDateTime , endDateTime + datetime.timedelta(minutes=2)):
            logger = getLogger()
            logger.info(
                "RF_queueNumberKeep: {},  setting: {} to {}".format("Resume Queue", startDateTime, endDateTime))
            msg = resumeQueueNumber()

            print(msg)

    print("--------------" * 10)


def changeQueueSetToRCS(queueDict):
    loginRCS()

    shipingSpaceService = Web_RCS.ShippingSpaceService()

    allocationService = Web_RCS.ShippingSpaceAllocationService()
    switchSpaceService = Web_RCS.ShippingHoleSwitchSpaceService()

    dataList = json.loads(shipingSpaceService.sendJSON().text)["data"]

    rcsQueueDict = {}

    msg = ""

    for data in dataList:
        if data["spaceText"] not in rcsQueueDict.keys():
            rcsQueueDict[data["spaceText"]] = {}
        rcsQueueDict[data["spaceText"]] = {"queueMax": data["queueMax"], "statusStr": data["statusStr"], "spaceCode": data["spaceCode"]}

    for spaceText, spaceInfo in queueDict.items():
        if spaceText not in rcsQueueDict.keys():
            continue

        if rcsQueueDict[spaceText]["queueMax"] != spaceInfo["queueMax"]:
            allocationService.setLocation(rcsQueueDict[spaceText]["spaceCode"])
            allocationService.setMaxQueue(spaceInfo["queueMax"])
            print(datetime.datetime.now())
            print("Switch queue Num\n")
            print(allocationService.params)
            allocationService.sendJSON()
            msg += "{}: {} to {}\n".format(spaceText, rcsQueueDict[spaceText]["queueMax"], spaceInfo["queueMax"])

        if rcsQueueDict[spaceText]["statusStr"] != spaceInfo["statusStr"]:
            switchSpaceService.setLocation(rcsQueueDict[spaceText]["spaceCode"])
            openClose = 0 if spaceInfo["statusStr"] == "Close" else 1
            switchSpaceService.setOpenClose(openClose)
            print(datetime.datetime.now())
            print("Switch Status\n")
            print(switchSpaceService.params)
            switchSpaceService.sendJSON()
            msg += "{}: {} to {}\n".format(spaceText, rcsQueueDict[spaceText]["statusStr"], spaceInfo["statusStr"])

    return msg

@exception_handler
def RF_queueSetEdit(*args):
    pastPickleDict = args[0]
    now = datetime.datetime.now()

    defaultSetName = ""

    for queueSetName, queueSetDict in pastPickleDict.items():
        if queueSetDict["isDefault"]:
            defaultSetName = queueSetName

    # sort timeDict By start Time


    for queueSetName, queueSetDict in pastPickleDict.items():
        if not queueSetDict["deployStatus"]["status"]:
            continue

        timeDict = queueSetDict["deployStatus"]["timeslot"]
        autoStatingTimeList = [timeDict]

        if not (timeDict["start"] and timeDict["end"]):
            continue

        for timeRangeDict in autoStatingTimeList:

            startTime = str((timeRangeDict["start"]))
            startMinute = int(startTime[-2:])
            startHour = int(startTime[:-2])
            startDateTime = now.replace(hour=startHour, minute=startMinute, second=0)

            startCheckTime = startTime
            startEditTime = startCheckTime

            endTime = str(int(timeRangeDict["end"]))
            endMinute = int(endTime[-2:])
            endHour = int(endTime[:-2])
            endDateTime = now.replace(hour=endHour, minute=endMinute, second=0)

            endCheckTime = endTime
            endEditTime = endCheckTime

            print(startTime, endTime)


            # Increase Queue
            if withInRange(now, startDateTime, startDateTime + datetime.timedelta(minutes=2)):
                print(queueSetName)
                print("{} start is activated".format(queueSetName))
                msg = changeQueueSetToRCS(queueSetDict["queueDict"])
                logger = getLogger()
                logger.info("RF_queueSetEdit: {}, setting: {} to {}".format("Increase Queue", startDateTime, endDateTime))
                print(msg)

            # resume Queue
            if withInRange(now, endDateTime , endDateTime + datetime.timedelta(minutes=2)):
                logger = getLogger()
                if defaultSetName:
                    print(queueSetName)
                    print("default: {}".format(defaultSetName))
                    print("{} end is activated".format(queueSetName))
                    defaultQueueDict = pastPickleDict[defaultSetName]["queueDict"]
                    msg = changeQueueSetToRCS(defaultQueueDict)

                    logger.info("RF_queueSetEdit: {},  setting: {} to {}".format("Resume Queue", startDateTime, endDateTime))

                    print(msg)
                else:
                    logger.info("no default is set")

        print("--------------" * 10)


# def addStagingNumMonitor(id, queueSetName, targetStagingNum):
#     msg = ""
#
#     fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["stagingNumMonitor"]
#     pastPickleDict = getStagingNumMonitorDictFromPickle(fileName)
#
#     queueSetFileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
#     queueSetDict = getQueueSetFromPickle(queueSetFileName)
#
#     if queueSetName not in queueSetDict.keys():
#         msg += "{} not in queueSetPickle [{}]".format(queueSetName, str(queueSetDict.keys()))
#         return msg
#
#     if len(pastPickleDict) >= 30:
#         msg += "too many sets in the pastPickleDict"
#         return msg
#
#     if id in pastPickleDict.keys():
#         msg += "{} is already saved".format(id)
#         return msg
#
#     stagingInfoServiceHi = RCS_Statistics.StagingInfoService()
#     currentStagingDict = stagingInfoServiceHi.getWorkingStagingDict()
#     maxStagingNum = currentStagingDict["total"]
#
#     if targetStagingNum > maxStagingNum:
#         msg += "target Staging Num {} is larger than Max Size {}".format(targetStagingNum, maxStagingNum)
#         return msg
#
#     newPickleDict = copy.deepcopy(pastPickleDict)
#
#     newPickleDict[id] = {"queueSetName": queueSetName, "targetStagingNum": targetStagingNum}
#
#     saveStagingNumMonitorDictFromPickle(newPickleDict, fileName)
#     msg += "{} is saved".format(id)
#     return msg



def getStagingNumMonitor():
    msg = "{}\n".format(datetime.datetime.now())

    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["stagingNumMonitor"]
    pastPickleDict = getStagingNumMonitorDictFromPickle(fileName)

    for id, monitorInfo in pastPickleDict.items():
        msg += "{} : queueSet: {}, stagingNum: {}\n".format(id, monitorInfo["queueSetName"], monitorInfo["targetStagingNum"])

    return msg

def clearStagingNumMonitor():
    msg = ""

    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["stagingNumMonitor"]
    newPickleDict = {}
    saveStagingNumMonitorDictFromPickle(newPickleDict, fileName)
    msg += "data is clean"
    return msg

# def RF_stagingNumMonitor(*args):
#     # pickle data Structure --> {"{datetime.datetime.now()_0/1/2}: ["queueSetName": "queueNameSet", "targetStagingNum": 30}}
#     pastPickleDict = args[0]
#     now = datetime.datetime.now()
#     stagingNumMonitorFileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["stagingNumMonitor"]
#
#     stagingInfoServiceHi = RCS_Statistics.StagingInfoService()
#     currentStagingDict = stagingInfoServiceHi.getWorkingStagingDict()
#
#     currentStagingNum = int(currentStagingDict["num"])
#
#     msg = "{}\n".format(datetime.datetime.now())
#
#     taskDict = {}
#
#     for taskId in pastPickleDict.keys():
#         idSplitList = taskId.split("_")
#         idDateTime = idSplitList[0]
#         idSeq = int(idSplitList[-1])
#
#         if idDateTime not in taskDict.keys():
#             taskDict[idDateTime] = []
#         taskDict[idDateTime].append(idSeq)
#
#     sortedTaskDict = {idDateTime: sorted(taskDict[idDateTime]) for idDateTime in taskDict.keys()}
#
#     for idDateTimeStr, seqList in sortedTaskDict.items():
#         executingTaskName = "{}_{}".format(idDateTimeStr, str(seqList[0]))
#
#         if executingTaskName not in pastPickleDict.keys():
#             logger = getLogger()
#             logger.error("{} not in pastPickleList [{}]".format(idDateTimeStr, str(pastPickleDict.keys())))
#             continue
#
#         monitorInfo = pastPickleDict[executingTaskName]
#
#         if int(seqList[0]) == 0:
#             # decrease queue Num
#             queueSetName = monitorInfo["queueSetName"]
#             updateQueueSetToRCS(queueSetName)
#             msg += "{} is activated".format(queueSetName)
#             mylogger = getLogger()
#             mylogger.info(msg)
#             # clear executed set
#             del pastPickleDict[executingTaskName]
#             saveStagingNumMonitorDictFromPickle(pastPickleDict, stagingNumMonitorFileName)
#
#         else:
#             if currentStagingNum <= int(monitorInfo["targetStagingNum"]):
#                 #resume
#                 queueSetName = monitorInfo["queueSetName"]
#                 updateQueueSetToRCS(queueSetName)
#                 msg += "{} is activated".format(queueSetName)
#                 mylogger = getLogger()
#                 mylogger.info(msg)
#                 del pastPickleDict[executingTaskName]
#                 saveStagingNumMonitorDictFromPickle(pastPickleDict, stagingNumMonitorFileName)
#
#
#
#     for id, monitorInfo in pastPickleDict.items():
#
#             idSplitList = id.split("_")
#             idDateTime = idSplitList[0]
#             idSeq = int(idSplitList[-1])
#
#             sameIdSeqList = [int(id.split["_"][-1]) for id in pastPickleDict.keys() if idDateTime in pastPickleDict.keys()]
#             minSeq = min(sameIdSeqList)
#
#             if idSeq == minSeq:
#                 #execute and delete
#                 queueSetName = monitorInfo["queueSetName"]
#                 updateQueueSetToRCS(queueSetName)
#                 msg += "{} is activated".format(queueSetName)
#                 mylogger = getLogger()
#                 mylogger.info(msg)
#                 print("")
#
#             print("{} active".format(queueSetName))


@exception_handler
def RF_dailyBatteryRecord(*args):
    autoBatteryRecordimeList = [{}, {}]
    autoBatteryRecordimeList = args[0]
    now = datetime.datetime.now()
    for recordTimeDateTime in autoBatteryRecordimeList:
        print("")
        #

def handleMsg(msg, bot, update):
    pass

@exception_handler
def RF_dailyStaging(*args):
    autoStatingTimeList = args[0]
    now = datetime.datetime.now()
    for timeRangeDict in autoStatingTimeList:
        isNight = isNightStaging(timeRangeDict)

        if isNight:
            editsStaging = editsStagingNight
            getStagingTime = getNightStagingTime
        else:
            editsStaging = editsStagingMorning
            getStagingTime = getMorningStagingTime

        startTime = str((timeRangeDict["start"]))
        startMinute = int(startTime[-2:])
        startHour = int(startTime[:-2])
        startDateTime = now.replace(hour=startHour, minute=startMinute, second=0)

        startCheckTime = startTime
        startEditTime = startCheckTime

        endTime = str((timeRangeDict["end"]))
        endMinute = int(endTime[-2:])
        endHour = int(endTime[:-2])
        endDateTime = now.replace(hour=endHour, minute=endMinute, second=0)

        endCheckTime = endTime
        endEditTime = str(int(endCheckTime) + 100)

        print(startTime, endTime)

        stepBystep = False
        if "stepBystep" in timeRangeDict.keys() and timeRangeDict["stepBystep"]:
            stepBystep = True

        txtStagingTime = getStagingTime()

        # open Staging
        if withInRange(now, startDateTime, endDateTime):
            if txtStagingTime["start"] != startEditTime and txtStagingTime["end"] != endEditTime:

                logger = getLogger()
                logger.info(
                    "RF_dailyStaging: {},  setting: {} to {}".format("Open Staging", startDateTime, endDateTime))
                editsStaging([startEditTime, endEditTime])
                print("{} - {} edit start".format(startTime, endTime))

        # close Staging
        if not withInRange(now, startDateTime, endDateTime):

            if txtStagingTime["start"] == startEditTime and txtStagingTime["end"] == endEditTime:
                logger = getLogger()
                logger.info(
                    "RF_dailyStaging: {},  setting: {} to {} , step By step ({})".format("Close Staging", startDateTime, endDateTime, stepBystep))

                if startEditTime == "-1" and endEditTime == "-1": # exceptional case
                    continue


                #Main Edit
                if stepBystep:
                    editsStaging([startCheckTime, endCheckTime])
                else:
                    editsStaging([-1, -1])
                print("{} - {} edit cancel".format(startTime, endTime))
def main():

    while True:

        for functionName in regularRouteList:

            functionLogicData = readFunctionPickleData(functionName)

            if not functionLogicData:
                # time.sleep(SLEEP_TIME)
                continue
            print(functionName)
            try:
                getFunction(functionName)(functionLogicData)
            except Exception as e:
                logError(str(e))


        time.sleep(SLEEP_TIME)







if __name__ == "__main__":
    logger = getLogger()
    main()