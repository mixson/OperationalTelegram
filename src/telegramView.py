from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, RegexHandler
import os, sys
currentDir = "\\".join(os.getcwd().split("\\")[0:-1])
sys.path.insert(0, currentDir)
# updater = Updater(token='1407640777:AAG1zlyYfk7QVpIJQonTv28TQG2dQM6jC9U', use_context=False) # production bot
# updater = Updater(token='1323516378:AAFEbQrv0AH8kZ3TU7dqq4ApO76pbqGMVvE', use_context=False) # testing bot
# updater = Updater(token='1828434617:AAEWhEfrq2eJt7TnF14EVBqmAdjDedsWctg', use_context=False) # jim_jim bot
# updater = Updater(token='1972257715:AAFo_buHhYp81NpQjS1ZwaeAg7gvGyOjMR4', use_context=False) #  d!R@tf+3^y\C bot(production)


updater = Updater(token='1993959700:AAExTRuoZwSPDFnxmEZou1SNx-STA9CKvOc', use_context=False) #  stagingTimeViewBot

buttonDictwithoutParams = {"getStagingTime": "CM_getStagingTime"}

buttonDictwithoutParamsDescription  = {"start": "CM_start"}

secretButtonDictParams = {}

buttonDictwithParams = {}

combinedButtonDict = {}
combinedButtonDict.update(buttonDictwithParams)
combinedButtonDict.update(buttonDictwithoutParams)
combinedButtonDict.update(secretButtonDictParams)

import ast
import time, datetime
import re
import logging
import pickle
import copy
import json
import traceback

from values import RCS_CONSTANT
from values.CONSTANT import INVERSE_BOUND_AREA, DATETIME_FORMAT, WORKING_STATION_DIVIDE, STATION_QUEUE_NUM
from utils.Web_Rcs import Web_RCS


loggingDirPath = os.path.join(currentDir, "log")

from values import RCS_CONSTANT

def send_message(bot, chat_id, text: str, **kwargs):
    if len(text) <= RCS_CONSTANT.MAX_MESSAGE_LENGTH:
        return bot.send_message(chat_id, text, parse_mode=ParseMode.HTML, **kwargs)

    parts = []
    while len(text) > 0:
        if len(text) > RCS_CONSTANT.MAX_MESSAGE_LENGTH:
            part = text[:RCS_CONSTANT.MAX_MESSAGE_LENGTH]
            first_lnbr = part.rfind('\n')
            if first_lnbr != -1:
                parts.append(part[:first_lnbr])
                text = text[first_lnbr:]
            else:
                parts.append(part)
                text = text[RCS_CONSTANT.MAX_MESSAGE_LENGTH:]
        else:
            parts.append(text)
            break

    msg = None
    for part in parts:
        msg = bot.send_message(chat_id, part, parse_mode=ParseMode.HTML, **kwargs)
        time.sleep(1)
    return msg  # return only the last message



def getClickButtonData(bot, update):
    try:
        print("getClickButtonData")
        current_module = sys.modules[__name__]
        print(update.callback_query.data)
        # clickRateDict = {"id": update.callback_query.message.chat.id, "button": update.callback_query.data, "time": datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}
        for button, data in combinedButtonDict.items():
            # print("test {}/ {}".format(update.callback_query.data, data)) # debug
            if update.callback_query.data == button:
                print(button + " is called")
                if button in buttonDictwithParams.keys():
                    update.callback_query.edit_message_text(data["msg"])
                msg = getattr(current_module, data)(bot, update) # calling target function
                print(msg)
                # bot.send_message(update)
                # update.callback_query.edit_message_text(msg)
                if isinstance(msg, str):
                    send_message(bot, str(update.callback_query.message.chat.id), msg)
                if isinstance(msg, list):
                    for part in msg:
                        chat_id = str(update.callback_query.message.chat.id)
                        bot.send_message(chat_id, part, parse_mode=ParseMode.HTML)
                reply_markup = InlineKeyboardMarkup(keyBoard) # keyboard global variable

                bot.send_message(str(update.callback_query.message.chat.id), 'Command:',
                                 reply_markup=reply_markup)
                break
        # logging.info('[getClickButtonData][callback_query data]: %s' % update.callback_query.data)
    except Exception as e:
        print(str(e))

def getKeyBoardWithoutParam(dict1):
    try:
        dict2 = {}
        tempdict1 = {}

        dict1KeyList = list(dict1.keys())
        dictKeyhalfLen = int(len(dict1KeyList) / 2)

        for i in range(len(dict1KeyList)):
            key = dict1KeyList[i]
            if i < dictKeyhalfLen:
                tempdict1[key] = dict1[key]
            else:
                dict2[key] = dict1[key]
        dict1 = tempdict1

        longerDict = dict1
        if len(dict2) >= len(dict1):
            longerDict = dict2
        tempList = []
        tempList2 = []
        dict1KeyList = list(dict1.keys())
        dict2KeyList = list(dict2.keys())
        for i in range(len(longerDict)):
            tempList.append([])

        for i in range(len(longerDict)):
            if i < len(dict1):
                # tempList[i].append(InlineKeyboardButton(dict1KeyList[i], callback_data=str(dict1[ dict1KeyList[i]])))
                tempList[i].append(InlineKeyboardButton(dict1KeyList[i], callback_data=str(dict1KeyList[i])))
            else:
                tempList[i].append(InlineKeyboardButton(" ", callback_data= " "))

            if i < len(dict2):
                # tempList[i].append(InlineKeyboardButton(dict2KeyList[i], callback_data=str(dict2[ dict2KeyList[i]]["cmd"])))
                tempList[i].append(InlineKeyboardButton(dict2KeyList[i], callback_data=str(dict2KeyList[i])))
            else:
                tempList[i].append(InlineKeyboardButton(" ", callback_data=" "))

        return tempList
    except Exception as e:
        print(str(e))

keyBoard = getKeyBoardWithoutParam(buttonDictwithoutParams)

def getFileFunctionName(filename):
    print(filename)
    with open(filename) as file:
        node = ast.parse(file.read())
    classes = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    return classes

def addTGHandler(updater, name, function):
    updater.dispatcher.add_handler(CommandHandler(name, function))

def initTGHandler(updater):
    current_module = sys.modules[__name__]
    allFunctionName = getFileFunctionName(__file__)
    for function in allFunctionName:
        functionName = function.name
        if "CM_" in functionName:
            tgCMD = functionName[3:]
            # print(tgCMD)
            addTGHandler(updater, tgCMD, getattr(current_module, functionName))

def getStagingDictFromPickle(fileName):
    if not os.path.exists(fileName):
        return list()
    if os.path.getsize(fileName) > 0:
        with open(fileName, "rb") as file:
            a = pickle.load(file)
            print(a)
        return a
    return list()






def getLogger():

    today = datetime.datetime.now()
    todayStr = "{}_{}_{}".format(today.year, today.month, today.day)
    fileName = "{}_{}.txt".format("DailyRouteLogTelegramView", "{}".format(todayStr))
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


@exception_handler
def CM_start(bot, update):
    """Send a message when the command /start is issued."""
    try:
        print("start")
        # reply_markup = InlineKeyboardMarkup([[
        #     InlineKeyboardButton(showMsg, callback_data= showMsg)] for showMsg, cmd in combinedButtonDict.items()])
        print(keyBoard)
        reply_markup = InlineKeyboardMarkup(keyBoard)
        print(reply_markup)
        bot.send_message(update.message.chat.id, 'Command:', reply_to_message_id=update.message.message_id,
                         reply_markup=reply_markup)

    except Exception as e:
        print(str(e))

@exception_handler
def CM_getRegularStaging(bot, update):
    print("1")
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["dailyStaging"]
    timeList = getStagingDictFromPickle(fileName)
    msg = ""
    for timeDict in timeList:

        msg += "{} - {}".format(timeDict["start"], timeDict["end"])
        msg += "\n"
    if not msg:
        msg = "empty"
    update.message.reply_text(msg, parse_mode='Markdown')

def getRegularStagingMsg():
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["dailyStaging"]
    timeList = getStagingDictFromPickle(fileName)
    msg = ""
    for timeDict in timeList:

        msg += "{} - {}".format(timeDict["start"], timeDict["end"])
        msg += "\n"
    if not msg:
        msg = "empty"

    return msg

def getMorningStagingTime():
    mrtaConfigLocation = RCS_CONSTANT.MRTA_CONFIG_LOCATION
    outputDict = {"start": None, "end": None}

    with open(mrtaConfigLocation, encoding="utf-8") as file:
        text = file.read()

        # targetList = ["<MRTA_SET_T>(.*)</MRTA_SET_T>",
        #               "<MRTA_SET_PICK_T>(.*)</MRTA_SET_PICK_T>", ]

        targetDict = {"start": "<MRTA_SET_T>(.*)</MRTA_SET_T>",
                      "end": "<MRTA_SET_PICK_T>(.*)</MRTA_SET_PICK_T>"}

        for key, target in targetDict.items():
            location = re.search(target, text)
            print(location)
            print(location.group(1))
            outputDict[key] = location.group(1)

    return outputDict

def getNightStagingTime():
    mrtaConfigLocation = RCS_CONSTANT.MRTA_CONFIG_LOCATION
    outputDict = {"start": None, "end": None}

    with open(mrtaConfigLocation, encoding="utf-8") as file:
        text = file.read()

        # targetList = ["<MRTA_SET_T_PM>(.*)</MRTA_SET_T_PM>",
        #               "<MRTA_SET_PICK_T_PM>(.*)</MRTA_SET_PICK_T_PM>",]

        targetDict = {"start": "<MRTA_SET_T_PM>(.*)</MRTA_SET_T_PM>",
                      "end": "<MRTA_SET_PICK_T_PM>(.*)</MRTA_SET_PICK_T_PM>"}



        for key, target in targetDict.items():

            location = re.search(target, text)
            print(location)
            print(location.group(1))
            outputDict[key] = location.group(1)

    return outputDict

@exception_handler
def CM_getMorningStagingTime(bot, update):
    timeSlotDict = getMorningStagingTime()
    msg = ""

    for key, timeResult in timeSlotDict.items():
        msg += "{}: {} ".format(key, timeResult)

    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
def CM_getNightStagingTime(bot, update):
    timeSlotDict = getNightStagingTime()
    msg = ""

    for key, timeResult in timeSlotDict.items():
        msg += "{}: {} ".format(key, timeResult)

    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
def CM_getStagingTime(bot, update):
    morngingTimeSlotDict = getMorningStagingTime()
    nightTimeSlotDict = getNightStagingTime()
    regularStagingTime = getRegularStagingMsg()

    msg = "{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    msg += "Morning Staging:\n"
    for key, timeResult in morngingTimeSlotDict.items():
        msg += "{}: {} ".format(key, timeResult)

    msg += "\n\n"

    msg += "Night Staging:\n"
    for key, timeResult in nightTimeSlotDict.items():
        msg += "{}: {} ".format(key, timeResult)

    msg += "\n\n"

    msg += "Regular Staging: \n"
    msg += regularStagingTime

    # send_message(bot, update, msg)
    return msg

@exception_handler
def CM_getLog(bot, update):
    try:
        msg = "{}\n".format(datetime.datetime.now())
        logger = getLogger()
        logFileName = logger.handlers[0].baseFilename

        with open(logFileName, "r+") as file:
            line = file.readline()
            msg += line

        update.message.reply_text(msg, parse_mode='Markdown')
        return msg

    except Exception as e:
        msg += str(e)
        update.message.reply_text(msg, parse_mode='Markdown')

if __name__ == "__main__":
    logger = getLogger()
    initTGHandler(updater)
    updater.dispatcher.add_handler(CallbackQueryHandler(getClickButtonData))
    # msg = CM_stationTaskDurationNight(0, 0)

    updater.start_polling()
    updater.idle()