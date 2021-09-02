import datetime
import logging
import os, sys
import traceback

currentDir = "\\".join(os.getcwd().split("\\")[0:-1])
sys.path.insert(0, currentDir)
loggingDirPath = os.path.join(currentDir, "logss")

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

if __name__ == "__main__":
    logger = getLogger()
    try:
        a = 1
        b = 0
        c = a/b
    except Exception as e:
        logError(str(e))