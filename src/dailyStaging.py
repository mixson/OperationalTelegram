import datetime, time

import os, sys
import logging
import pickle
currentDir = "\\".join(os.getcwd().split("\\")[0:-1])
sys.path.insert(0, currentDir)

from src.telegramBot import editsStagingMorning, editsStagingNight, getMorningStagingTime, getNightStagingTime
from values.RCS_CONSTANT import STAGINGPICKE_FILENAME


loggingDirPath = os.path.join(currentDir, "log")



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
    fileName = "{}_{}.txt".format("StagingLog", "{}".format(todayStr))
    # config
    logging.captureWarnings(True)
    formatter = logging.Formatter('[%(asctime)s] (%(levelname)s) %(message)s')
    myLogger = logging.getLogger("py.warnings")
    myLogger.setLevel(logging.INFO)

    if not os.path.exists(loggingDirPath):
        os.makedirs(loggingDirPath)

    fileHandler = logging.FileHandler(os.path.join(loggingDirPath, fileName))
    fileHandler.setFormatter(formatter)
    myLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    myLogger.addHandler(consoleHandler)

    return myLogger

def getStagingDictFromPickle(fileName):
    if os.path.getsize(fileName) > 0:
        with open(fileName, "rb") as file:
            a = pickle.load(file)
            print(a)
        return a
    return None

regularRouteList = ["dailyStaging", "queueNumberKeep"]

functionDict = {"dailyStaging": None, "queueNumberKeep": None}
functionTimeDict = {"dailyStaging": None, "queueNumberKeep": None}


if __name__ == "__main__":
    logger = getLogger()
    fileName = STAGINGPICKE_FILENAME
    while True:
        autoStatingTimeList = getStagingDictFromPickle(fileName)
        openDict = {str(timeRange): True for timeRange in autoStatingTimeList}
        try:
            now = datetime.datetime.now()
            for timeRangeDict in autoStatingTimeList:
                isNight = isNightStaging(timeRangeDict)

                if isNight:
                    editsStaging = editsStagingNight
                    getStagingTime = getNightStagingTime
                else:
                    editsStaging = editsStagingMorning
                    getStagingTime = getMorningStagingTime


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
                endEditTime = str(int(endCheckTime) + 100)

                print(startTime, endTime)

                txtStagingTime = getStagingTime()

                # open Staging
                if withInRange(now, startDateTime, endDateTime):
                    if txtStagingTime["start"] != startEditTime and txtStagingTime["end"] != endEditTime:
                        editsStaging([startEditTime, endEditTime])
                        print("{} - {} edit start".format(startTime, endTime))

                # close Staging
                if not withInRange(now, startDateTime, endDateTime):
                    if txtStagingTime["start"] == startEditTime and txtStagingTime["end"] == endEditTime:
                        editsStaging([-1, -1])
                        print("{} - {} edit cancel".format(startTime, endTime))

            print("--------------" * 10)
            time.sleep(1)
        except Exception as e:
            print(str(e))
            logger.info(str(e))
        # except Exception as e:
        #     print(str(e))