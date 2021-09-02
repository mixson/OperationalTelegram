from src.dailyRoute import addStagingNumMonitor, getStagingNumMonitor, clearStagingNumMonitor
from values import CONSTANT

import datetime

if __name__ == "__main__":
    currentTime = datetime.datetime.now()
    currentTimeStr = currentTime.strftime(CONSTANT.DATETIME_FORMAT)

    startId = "{}_{}".format(currentTimeStr, "0")
    startQueueSet = "lunch"
    startTargetStagingNum = 30

    endId = "{}_{}".format(currentTimeStr, "1")
    endQueueSet = "midnight"
    endTargetStagingNum = 10

    clearStagingNumMonitor()

    addStagingNumMonitor(startId, startQueueSet, startTargetStagingNum)
    addStagingNumMonitor(endId, endQueueSet, endTargetStagingNum)

    msg = getStagingNumMonitor()
    print("")