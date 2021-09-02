from utils.Web_Rcs import Web_RCS

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, RegexHandler
import os, sys
currentDir = "\\".join(os.getcwd().split("\\")[0:-1])
sys.path.insert(0, currentDir)
# updater = Updater(token='1407640777:AAG1zlyYfk7QVpIJQonTv28TQG2dQM6jC9U', use_context=False) # production bot
# updater = Updater(token='1323516378:AAFEbQrv0AH8kZ3TU7dqq4ApO76pbqGMVvE', use_context=False) # testing bot

import ast
import time, datetime
import re
import logging
import pickle
import copy
import json

from values import RCS_CONSTANT
from values.CONSTANT import INVERSE_BOUND_AREA, DATETIME_FORMAT
from utils.Web_Rcs import Web_RCS


# dict data Structure
#
a = {"A": {"deployStatus": {"status": "open", "timeslot": {"start": 1200, "end": 1200}}, "queueDict": {"MOUT01": {"queueNum": 3, "statusStr": "open"}}}}

def getLogger():

    today = datetime.datetime.now()
    todayStr = "{}_{}_{}".format(today.year, today.month, today.day)
    fileName = "{}_{}.txt".format("OPLog", "{}".format(todayStr))
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

def CM_createQueueSet(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()
    inputList = []
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-1]
    setName = clearedInputText
    print(clearedInputText)

    pastPickleDict = getStagingDictFromPickle(fileName)

    if setName in pastPickleDict.keys():
        msg = "{} already set".format(setName)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg


    try:
        loginRCS()
        shippingSpaceService = Web_RCS.ShippingSpaceService()
        queueList = shippingSpaceService.sendJSON()["data"]
        queueDict = {}
        for queue in queueList:
            spaceText = queue["spaceText"]
            if spaceText not in queueDict.keys():
                queueDict[spaceText] = {}
            spaceDict = queueDict[spaceText]
            spaceDict["queueMax"] = queue["queueMax"]
            spaceDict["statusStr"] = queue["statusStr"]



    except Exception() as e:
        msg = str(e)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg

    pastPickleDict[setName] = {"queueDict": queueDict,
                               "deployStatus": {"status": "stopped", "timeslot": {"start": None, "end": None}}}

    saveQueueSetToPickle(pastPickleDict, fileName)



    msg = ""

    for workingTimeDict in workingList:
        msg += "{} - {}\n".format(workingTimeDict["start"], workingTimeDict["end"])

    print(msg)
    update.message.reply_text(msg, parse_mode='Markdown')

def CM_copyQueueSet(bot, update):
    pass

def CM_deleteQueueSet(bot, update):
    pass

def CM_showQueueSet(bot, update):
    pass

def CM_showQueueSetStatus(bot, update):
    pass

def CM_editQueueSet(bot, update):
    pass

def deployQueueSet(bot, update):
    pass

def stopQueueSet(bot, update):
    pass


def loginRCS():
    rcs = Web_RCS()
    loginService = rcs.getLoginService()
    loginService.runService()


if __name__ == "__main__":
    pass