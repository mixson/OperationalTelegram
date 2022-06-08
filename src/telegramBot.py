from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, RegexHandler
import os, sys
currentDir = "\\".join(os.getcwd().split("\\")[0:-1])
sys.path.insert(0, currentDir)
# updater = Updater(token='1407640777:AAG1zlyYfk7QVpIJQonTv28TQG2dQM6jC9U', use_context=False) # production bot
# updater = Updater(token='1323516378:AAFEbQrv0AH8kZ3TU7dqq4ApO76pbqGMVvE', use_context=False) # testing bot
# updater = Updater(token='1828434617:AAEWhEfrq2eJt7TnF14EVBqmAdjDedsWctg', use_context=False) # jim_jim bot
# updater = Updater(token='1972257715:AAFo_buHhYp81NpQjS1ZwaeAg7gvGyOjMR4', use_context=False) #  d!R@tf+3^y\C bot(production)
updater = Updater(token='5201936161:AAHPaj3wYQq1SA-io7ZmNOE_xg0IepnZyqs', use_context=False) #  bZRfAnnUnx_bot(production)


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
from utils.Paramiko_SSH import LowerBatteryService, ShutDownAGVService

buttonDictwithoutParams = {"show time": "CM_showTime",
                           "hello World": "CM_helloWorld",
                           "Subscribe": "CM_subscribeQueueNotification",
                           "test": "CM_sendMsgToSubscriptionList"}

buttonDictwithoutParamsDescription  = {"start": "CM_start"}

secretButtonDictParams = {}

buttonDictwithParams = {}

combinedButtonDict = {}
combinedButtonDict.update(buttonDictwithParams)
combinedButtonDict.update(buttonDictwithoutParams)
combinedButtonDict.update(secretButtonDictParams)

loggingDirPath = os.path.join(currentDir, "log")

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

def getLogger():

    today = datetime.datetime.now()
    todayStr = "{}_{}_{}".format(today.year, today.month, today.day)
    fileName = "{}_{}.txt".format("DailyRouteLogTelegram", "{}".format(todayStr))
    # config
    # logging.captureWarnings(True)
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

def getRouteLogger():

    today = datetime.datetime.now()
    todayStr = "{}_{}_{}".format(today.year, today.month, today.day)
    fileName = "{}_{}.txt".format("DailyRouteLog", "{}".format(todayStr))
    # config
    # logging.captureWarnings(True)
    formatter = logging.Formatter('[%(asctime)s] (%(levelname)s) %(message)s')
    myLogger = logging.getLogger("py.warnings2")
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

    # file Handler
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

def addTGHandler(updater, name, function):
    updater.dispatcher.add_handler(CommandHandler(name, function))

def getFileFunctionName(filename):
    print(filename)
    with open(filename) as file:
        node = ast.parse(file.read())
    classes = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    return classes

def withInRange(data, start, end):
    if data >= start and data <= end:
        return True
    return False

def initTGHandler(updater):
    current_module = sys.modules[__name__]
    allFunctionName = getFileFunctionName(__file__)
    for function in allFunctionName:
        functionName = function.name
        if "CM_" in functionName:
            tgCMD = functionName[3:]
            # print(tgCMD)
            addTGHandler(updater, tgCMD, getattr(current_module, functionName))

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


def handleMsg(bot, update, msg): # for typing command -- handling


    if not update:
        print(msg)
        return msg

    if hasattr(update.message, "reply_text"):
        send_message(bot, str(update.message.chat.id), msg)
        # update.message.reply_text(msg)
        global combinedButtonDict
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(showMsg, callback_data=showMsg)] for showMsg, cmd in combinedButtonDict.items()])

        bot.send_message(str(update.message.chat.id), 'Command:',
                         reply_markup=reply_markup)

    logger = getLogger()
    # userInfoDict = {"chatId": update.effective_message.id, "messageId": update.message.message_id, "userName": update.message.username}
    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(msg, userInfoLog)
    logger.info(str(loggingMsg))

keyBoard = getKeyBoardWithoutParam(buttonDictwithoutParams)

def saveStagingDictToPickle(data, fileName):
    with open(fileName, "wb") as file:
        pickle.dump(data, file)
    print("{} is saved".format(str(data)))

def getStagingDictFromPickle(fileName):
    if not os.path.exists(fileName):
        return list()
    if os.path.getsize(fileName) > 0:
        with open(fileName, "rb") as file:
            a = pickle.load(file)
            print(a)
        return a
    return list()

def getQueueSetFromPickle(fileName):
    if not os.path.exists(fileName):
        return dict()
    if os.path.getsize(fileName) > 0:
        with open(fileName, "rb") as file:
            a = pickle.load(file)
            print(a)
        return a
    return dict()

def saveQueueSetToPickle(data, fileName):
    with open(fileName, "wb") as file:
        pickle.dump(data, file)
    print("{} is saved".format(str(data)))

def saveSubscriptionListToPickle(data, fileName):
    with open(fileName, "wb") as file:
        pickle.dump(data, file)
    print("{} is saved".format(str(data)))

def getSubscriptionListFromPickle(fileName):
    if not os.path.exists(fileName):
        return list()
    if os.path.getsize(fileName) > 0:
        with open(fileName, "rb") as file:
            a = pickle.load(file)
            print(a)
        return a
    return list()

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

@exception_handler
@logUserRecord
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
@logUserRecord
def CM_showTime(bot, update):
    now = datetime.datetime.now()
    print(now)
    handleMsg(bot, update, str(now))
    return str(now)

@exception_handler
@logUserRecord
def CM_helloWorld(bot, update):
    handleMsg(bot, update, "Hello World")
    return "Hello World"

def editsStagingMorning(timeList):
    mrtaConfigLocation = RCS_CONSTANT.MRTA_CONFIG_LOCATION

    def validateMorningInput(timeList):
        try:
            startTime = timeList[0]
            endTime = timeList[1]

            if not isinstance(startTime, int):
                startTime = int(startTime)

            if not isinstance(endTime, int):
                endTime = int(endTime)

            if not (startTime >= 100 or startTime <= 1200):
                raise Exception("length of input wrong {}".format(startTime))

            if not (endTime >= 100 or endTime <= 1200):
                raise Exception("length of input wrong {}".format(endTime))

            return True

        except Exception as e:
            print(str(e))
            return False


    msg = ""
    if not validateMorningInput(timeList):
        return False

    with open(mrtaConfigLocation, encoding="utf-8") as file:
        text = file.read()

        targetList = ["<MRTA_SET_T>(.*)</MRTA_SET_T>",
                      "<MRTA_SET_PICK_T>(.*)</MRTA_SET_PICK_T>",]

        replaceList = ["<MRTA_SET_T>{}</MRTA_SET_T>".format(timeList[0]),
                       "<MRTA_SET_PICK_T>{}</MRTA_SET_PICK_T>".format(timeList[1]),]

        targetResultDict = {}
        for i in range(len(targetList)):
            target = targetList[i]
            location = re.search(target, text)
            print(location)
            print(location.group(1))

            text = re.sub(target, replaceList[i], text)

            location = re.search(target, text)
            print(location)
            print(location.group(1))
            print("")

    print("")
    with open(mrtaConfigLocation, "w", encoding="utf-8") as file:
        file.write(text)

    # edit succesfully
    return True

@exception_handler
@logUserRecord
def CM_stagingEditMorning(bot, update):
    try:
        print("CM_stagingEditMorning")
        hourList = [i for i in range(13)]
        minuteList = [i for i in range(60)]



    except Exception as e:
        print(str(e))

def editsStagingNight(timeList):
    mrtaConfigLocation = RCS_CONSTANT.MRTA_CONFIG_LOCATION

    def validateMorningInput(timeList):
        try:
            startTime = timeList[0]
            endTime = timeList[1]

            if not isinstance(startTime, int):
                startTime = int(startTime)

            if not isinstance(endTime, int):
                endTime = int(endTime)

            if not (startTime >= 1200 or startTime <= 2400):
                raise Exception("length of input wrong {}".format(startTime))

            if not (endTime >= 1200 or endTime <= 2400):
                raise Exception("length of input wrong {}".format(endTime))

            return True

        except Exception as e:
            print(str(e))
            return False


    msg = ""
    if not validateMorningInput(timeList):
        return False

    with open(mrtaConfigLocation, encoding="utf-8") as file:
        text = file.read()

        targetList = ["<MRTA_SET_T_PM>(.*)</MRTA_SET_T_PM>",
                      "<MRTA_SET_PICK_T_PM>(.*)</MRTA_SET_PICK_T_PM>",]

        replaceList = ["<MRTA_SET_T_PM>{}</MRTA_SET_T_PM>".format(timeList[0]),
                       "<MRTA_SET_PICK_T_PM>{}</MRTA_SET_PICK_T_PM> ".format(timeList[1]),]

        targetResultDict = {}
        for i in range(len(targetList)):
            target = targetList[i]
            location = re.search(target, text)
            print(location)
            print(location.group(1))

            text = re.sub(target, replaceList[i], text)

            location = re.search(target, text)
            print(location)
            print(location.group(1))
            print("")

    print("")
    with open(mrtaConfigLocation, "w", encoding="utf-8") as file:
        file.write(text)

    # edit succesfully
    return True

@exception_handler
@logUserRecord
def CM_stagingEditNight(bot, update):
    try:
        print("CM_stagingEditNight")


    except Exception as e:
        print(str(e))

@exception_handler
@logUserRecord
def CM_hello(bot, update):
    print("hello")

@exception_handler
@logUserRecord
def CM_morningStaging(bot, update):
    logger = getLogger()

    id = update.message.text.replace('/info_', '')
    inputList = []
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-2:]
    print(clearedInputText)
    msg = ""
    if editsStagingMorning(clearedInputText):
        print("s")
    else:
        print("f")
    update.message.reply_text(id, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_nightStaging(bot, update):
    logger = getLogger()

    id = update.message.text.replace('/info_', '')
    inputList = []
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-2:]
    print(clearedInputText)
    if editsStagingNight(clearedInputText):
        print("s")
    else:
        print("f")
    update.message.reply_text(id, parse_mode='Markdown')

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
@logUserRecord
def CM_getRegularStaging(bot, update):
    print("1")
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["dailyStaging"]
    timeList = getStagingDictFromPickle(fileName)
    msg = ""
    for timeDict in timeList:

        msg += "{} - {}".format(timeDict["start"], timeDict["end"])
        if "stepBystep" in timeDict.keys():
            msg += "\t   stepBystep: {}".format(timeDict["stepBystep"])
        msg += "\n"
    if not msg:
        msg = "empty"
    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_addRegularStaging(bot, update):
    try:
        logger = getLogger()
        fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["dailyStaging"]


        inputList = []
        inputText = update.message.text

        userInfoLog = str(update.effective_message.chat)
        loggingMsg = "{}\n{}".format(inputText, userInfoLog)
        logger.info(loggingMsg)

        clearedInputText = inputText.split(" ")[1:]
        print(clearedInputText)
        start = int(clearedInputText[0])
        end = int(clearedInputText[1])

        timeDict = {"start": clearedInputText[0], "end": clearedInputText[1]}

        if len(clearedInputText) == 3:
            if clearedInputText[2] == "0":
                timeDict["stepBystep"] = False
            if clearedInputText[2] == "1":
                timeDict["stepBystep"] = True

        pastStagingList = getStagingDictFromPickle(fileName)

        workingStagingList = []
        if pastStagingList:
            workingStagingList = copy.deepcopy(pastStagingList)

        repeated = False

        for pastTimeDict in pastStagingList:
            if pastTimeDict["start"] == timeDict["start"] and pastTimeDict["end"] == timeDict["end"]:
                repeated = True

        if not repeated:
            workingStagingList.append(timeDict)

        saveStagingDictToPickle(workingStagingList, fileName)

        msg = ""

        for workingTimeDict in workingStagingList:
            msg += "{} - {}\n".format(workingTimeDict["start"], workingTimeDict["end"])

        update.message.reply_text(msg, parse_mode='Markdown')
    except Exception as e:
        print(e)
        logger = getLogger()
        msg += str(e)
        update.message.reply_text(msg, parse_mode='Markdown')
        logger.error(msg)


@exception_handler
@logUserRecord
def CM_clearRegularStaging(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["dailyStaging"]

    logger = getLogger()
    inputList = []
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    workingStagingList = []

    saveStagingDictToPickle(workingStagingList, fileName)

    msg = "cleared"

    for workingTimeDict in workingStagingList:
        msg += "{} - {}\n".format(workingTimeDict["start"], workingTimeDict["end"])

    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_deleteRegularStaging(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["dailyStaging"]

    logger = getLogger()
    inputList = []
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-2:]
    print(clearedInputText)

    timeDict = {"start": clearedInputText[0], "end": clearedInputText[1]}

    pastStagingList = getStagingDictFromPickle(fileName)

    workingStagingList = []
    if pastStagingList:
        workingStagingList = copy.deepcopy(pastStagingList)

    repeated = False

    for pastTimeDict in pastStagingList:
        if pastTimeDict["start"] == timeDict["start"] and pastTimeDict["end"] == timeDict["end"]:
            workingStagingList.remove(pastTimeDict)

    saveStagingDictToPickle(workingStagingList, fileName)

    msg = ""

    for workingTimeDict in workingStagingList:
        msg += "{} - {}\n".format(workingTimeDict["start"], workingTimeDict["end"])

    update.message.reply_text(msg, parse_mode='Markdown')


@exception_handler
@logUserRecord
def CM_getMorningStagingTime(bot, update):
    timeSlotDict = getMorningStagingTime()
    msg = ""

    for key, timeResult in timeSlotDict.items():
        msg += "{}: {} ".format(key, timeResult)

    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_getNightStagingTime(bot, update):
    timeSlotDict = getNightStagingTime()
    msg = ""

    for key, timeResult in timeSlotDict.items():
        msg += "{}: {} ".format(key, timeResult)

    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_addRegularQueue(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueNumberKeep"]
    logger = getLogger()
    inputList = []
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-2:]
    print(clearedInputText)

    timeDict = {"start": clearedInputText[0], "end": clearedInputText[1]}

    pastList = getStagingDictFromPickle(fileName)

    workingList = []
    if pastList:
        workingList = copy.deepcopy(pastList)

    repeated = False

    for pastTimeDict in pastList:
        if pastTimeDict["start"] == timeDict["start"] and pastTimeDict["end"] == timeDict["end"]:
            repeated = True

    if not repeated:
        workingList.append(timeDict)

    saveStagingDictToPickle(workingList, fileName)

    msg = ""

    for workingTimeDict in workingList:
        msg += "{} - {}\n".format(workingTimeDict["start"], workingTimeDict["end"])

    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_deleteRegularQueue(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueNumberKeep"]

    logger = getLogger()
    inputList = []
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-2:]
    print(clearedInputText)

    timeDict = {"start": clearedInputText[0], "end": clearedInputText[1]}

    pastStagingList = getStagingDictFromPickle(fileName)

    workingStagingList = []
    if pastStagingList:
        workingStagingList = copy.deepcopy(pastStagingList)

    repeated = False

    for pastTimeDict in pastStagingList:
        if pastTimeDict["start"] == timeDict["start"] and pastTimeDict["end"] == timeDict["end"]:
            repeated = True

    if repeated:
        workingStagingList.remove(timeDict)

    saveStagingDictToPickle(workingStagingList, fileName)

    msg = ""

    for workingTimeDict in workingStagingList:
        msg += "{} - {}\n".format(workingTimeDict["start"], workingTimeDict["end"])

    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_getRegularQueue(bot, update):
    print("1")
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueNumberKeep"]
    timeList = getStagingDictFromPickle(fileName)
    msg = ""
    for timeDict in timeList:

        msg += "{} - {}".format(timeDict["start"], timeDict["end"])
        msg += "\n"
    if not msg:
        msg = "empty"
    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_clearRegularQueue(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueNumberKeep"]

    logger = getLogger()
    inputList = []
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    workingStagingList = []

    saveStagingDictToPickle(workingStagingList, fileName)

    msg = "cleared"

    for workingTimeDict in workingStagingList:
        msg += "{} - {}\n".format(workingTimeDict["start"], workingTimeDict["end"])

    update.message.reply_text(msg, parse_mode='Markdown')




def refineStagingStrategyAddInput(stagingDict):
    pass

def validateStagingStrategyAddInput(stagingDict):
    pass

def CM_webStaging(bot, update):
    msg = "{}\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    loginRCS()

    inputText = update.message.text

    params = {"start": "", "end": "", "freeTime": "", "freeInterval": ""}


    targetParamsList = inputText.split(" ")[1:]

    dictKeyList = list(params.keys())
    for i in range(len(targetParamsList)):
        params[dictKeyList[i]] = targetParamsList[i]

    for keyName, value in params.items():
        pass


def getStationStatusDict():
    loginRCS()
    droppingHoleService = Web_RCS.DroppingHoleService()

    dataList = json.loads(droppingHoleService.sendJSON().text)["data"]

    stationDict = {}

    for data in dataList:
        if data["holeText"] not in stationDict.keys():
            stationDict[data["holeText"]] = {"holeCode": data["holeText"], "queueMax": data["queueMax"],
                                       "statusStr": data["statusStr"], "status": data["status"]}

    return stationDict

@exception_handler
@logUserRecord
def CM_getStationStatus(bot, update):
    stationDict = getStationStatusDict()
    stationQueueNumDict = STATION_QUEUE_NUM

    msg = "{}\n\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    for fingerName, stationList in WORKING_STATION_DIVIDE.items():
        msg += "{}\n".format(fingerName)
        for stationName in stationList:
            queueDifference = int(stationQueueNumDict[stationName]) - int(stationDict[stationName]["queueMax"])
            msg += "    \t{}: {} |{}| ({})\n".format(stationName, stationDict[stationName]["queueMax"], queueDifference,
                                                     stationDict[stationName]["statusStr"])
        msg += "\n"

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg

@exception_handler
@logUserRecord
def CM_editStationNum(bot, update):

    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-2:]

    queueNum = clearedInputText[0]
    stationNum = clearedInputText[1]

    msg = editStation(stationNum, queueNum)

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg



def editStation(queueNum, rules):
    commonRegexRules = rules

    rcs = Web_RCS()
    loginService = rcs.getLoginService()
    loginService.runService()

    editedSpaceList = []

    droppingHoleService = Web_RCS.DroppingHoleService()
    response = droppingHoleService.sendJSON()

    dataList = json.loads(response.text)["data"]

    for data in dataList:
        if re.match(commonRegexRules, data["holeText"]):
            editedSpaceList.append(data)

    msg = ""

    if int(queueNum) < 0:
        msg += "Error Queue < 0"
        return msg

    for location in editedSpaceList:
        if int(queueNum) > 0:
            droppingHoleAllocationService = Web_RCS.DroppingSpaceAllocationService()
            spaceCode = location["holeCode"]
            droppingHoleAllocationService.setLocation(spaceCode)
            droppingHoleAllocationService.setMinQueue(queueNum).setMaxQueue(queueNum)
            droppingHoleAllocationService.sendJSON()
            msg += "{}: {} to {}\n".format(location["holeText"], location["queueMax"], queueNum)
        # if int(queueNum) == 0:
        #     droppingHoleSwitchService = Web_RCS.DroppingSpaceSwitchService()
        #     spaceCode = location["holeCode"]
        #     droppingHoleSwitchService.setLocation(spaceCode)
        #     droppingHoleSwitchService.setOpenClose(queueNum)
        #     droppingHoleSwitchService.sendJSON()
        #     msg += "{}: {} to {}\n".format(location["holeText"], location["queueMax"], queueNum)


    return msg

def editStationOpen(openClose, rules):
    commonRegexRules = rules

    rcs = Web_RCS()
    loginService = rcs.getLoginService()
    loginService.runService()

    editedSpaceList = []

    droppingHoleService = Web_RCS.DroppingHoleService()
    response = droppingHoleService.sendJSON()

    dataList = json.loads(response.text)["data"]

    for data in dataList:
        if re.match(commonRegexRules, data["holeText"]):
            editedSpaceList.append(data)

    droppingHoleOpenCloseService = Web_RCS.DroppingSpaceSwitchService()

    msg = ""

    for location in editedSpaceList:
        spaceCode = location["holeCode"]
        droppingHoleOpenCloseService.setLocation(spaceCode)
        droppingHoleOpenCloseService.setOpenClose(0 if openClose == "0" else 1)
        droppingHoleOpenCloseService.sendJSON()
        openCloseStr = "Close" if openClose == "0" else "Open"
        msg += "{}: {} to {}\n".format(location["holeText"], location["statusStr"], openCloseStr)

    return msg

@exception_handler
@logUserRecord
def CM_editStationOpen(bot, update):
    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-2:]

    stationName = clearedInputText[0]
    openClose = clearedInputText[1]

    msg = editStationOpen(openClose, stationName)

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg


def editBound(queueNum, rules):
    commonRegexRules = rules

    rcs = Web_RCS()
    loginService = rcs.getLoginService()
    loginService.runService()

    editedSpaceList = []

    shippingHoleService = Web_RCS.ShippingSpaceService()
    response = shippingHoleService.sendJSON()

    dataList = json.loads(response.text)["data"]

    for data in dataList:
        if re.match(commonRegexRules, data["spaceText"]):
            editedSpaceList.append(data)



    msg = ""

    if int(queueNum) < 0:
        msg += "Error Queue < 0"
        return msg

    for location in editedSpaceList:
        if int(queueNum) > 0:
            shippingHoleAllocationService = Web_RCS.ShippingSpaceAllocationService()
            spaceCode = location["spaceCode"]
            shippingHoleAllocationService.setLocation(spaceCode)
            shippingHoleAllocationService.setMinQueue(queueNum).setMaxQueue(queueNum)
            shippingHoleAllocationService.sendJSON()
            msg += "{}: {} to {}\n".format(location["spaceText"], location["queueMin"], queueNum)
        # if int(queueNum) == 0:
        #     shippingHoleSwitchSpaceService = Web_RCS.ShippingHoleSwitchSpaceService()
        #     spaceCode = location["spaceCode"]
        #     shippingHoleSwitchSpaceService.setLocation(spaceCode)
        #     shippingHoleSwitchSpaceService.setOpenClose(queueNum).setMaxQueue(queueNum)
        #     shippingHoleSwitchSpaceService.sendJSON()
        #     msg += "{}: {} to {}\n".format(location["spaceText"], location["queueMin"], queueNum)


    return msg

def editBondOpenClose(openClose, rules):
    commonRegexRules = rules

    rcs = Web_RCS()
    loginService = rcs.getLoginService()
    loginService.runService()

    editedSpaceList = []

    shippingHoleService = Web_RCS.ShippingSpaceService()
    response = shippingHoleService.sendJSON()

    dataList = json.loads(response.text)["data"]

    for data in dataList:
        if re.match(commonRegexRules, data["spaceText"]):
            editedSpaceList.append(data)

    shippingHoleOpenCloseService = Web_RCS.ShippingHoleSwitchSpaceService()

    msg = ""


    for location in editedSpaceList:
        spaceCode = location["spaceCode"]
        shippingHoleOpenCloseService.setLocation(spaceCode)
        shippingHoleOpenCloseService.setOpenClose(openClose)
        shippingHoleOpenCloseService.sendJSON()
        msg += "{}: {} to {}\n".format(location["spaceText"], location["statusStr"], openClose)

    return msg

def editBoundByList(queueNum, conditionList):


    rcs = Web_RCS()
    loginService = rcs.getLoginService()
    loginService.runService()

    editedSpaceList = []

    shippingHoleService = Web_RCS.ShippingSpaceService()
    response = shippingHoleService.sendJSON()

    dataList = json.loads(response.text)["data"]

    for data in dataList:
        if data["spaceText"] in conditionList:
            editedSpaceList.append(data)

    shippingHoleAllocationService = Web_RCS.ShippingSpaceAllocationService()

    msg = ""

    if int(queueNum) <= 0:
        msg += "Error Queue <= 0"
        return msg

    for location in editedSpaceList:
        spaceCode = location["spaceCode"]
        shippingHoleAllocationService.setLocation(spaceCode)
        shippingHoleAllocationService.setMinQueue(queueNum).setMaxQueue(queueNum)
        shippingHoleAllocationService.sendJSON()
        msg += "{}: {} to {}\n".format(location["spaceText"], location["queueMin"], queueNum)

    return msg

def editBoundQueueNumberEast(queueNum):
    commonRegexRules = "^RMIN"
    msg = editBound(queueNum, commonRegexRules)
    return msg

@exception_handler
@logUserRecord
def CM_editBoundQueueNumberEast(bot, update):

    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-1:]

    queueNum = clearedInputText[0]

    commonRegexRules = "^RMIN"
    msg = editBoundQueueNumberEast(queueNum)

    update.message.reply_text(msg, parse_mode='Markdown')



def editBoundQueueNumberWest(queueNum):
    def numberToDigit(number):
        if number < 10 and number > 0:
            return "0{}".format(number)
        return str(number)

    commonRegexRules = "^LMIN(0[4-9]|1[0-9])$"
    # numberList = range(4,20)
    # locationList = ["LMIN{}".format(numberToDigit(number)) for number in numberList]
    msg = editBound(queueNum, commonRegexRules)
    return msg

@exception_handler
@logUserRecord
def CM_editBoundQueueNumberWest(bot, update):
    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-1:]

    queueNum = clearedInputText[0]

    msg = editBoundQueueNumberWest(queueNum)

    update.message.reply_text(msg, parse_mode='Markdown')

def editBoundQueueNumberNorth(queueNum):
    commonRegexRules = "^MOUT"
    msg = editBound(queueNum, commonRegexRules)
    return msg

@exception_handler
@logUserRecord
def CM_editBoundQueueNumberNorth(bot, update):
    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-1:]

    queueNum = clearedInputText[0]

    msg = editBoundQueueNumberNorth(queueNum)
    update.message.reply_text(msg, parse_mode='Markdown')

def editBoundQueueNumberNA(queueNum):
    commonRegexRules = "^MOUT0[1-4]"
    msg = editBound(queueNum, commonRegexRules)
    return msg

@exception_handler
@logUserRecord
def CM_editBoundQueueNumberNA(bot, update):
    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-1:]

    queueNum = clearedInputText[0]

    msg = editBoundQueueNumberNA(queueNum)
    update.message.reply_text(msg, parse_mode='Markdown')

def editBoundQueueNumberNB(queueNum):
    commonRegexRules = "^MOUT0[4-9]|^MOUT1[0-9]"
    msg = editBound(queueNum, commonRegexRules)
    return msg

@exception_handler
@logUserRecord
def CM_editBoundQueueNumberNB(bot, update):
    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-1:]

    queueNum = clearedInputText[0]

    msg = editBoundQueueNumberNB(queueNum)
    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_editBoundQueueNumberGTM(bot, update):
    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-1:]

    queueNum = clearedInputText[0]

    msg = editBoundQueueNumberNorth(queueNum)
    update.message.reply_text(msg, parse_mode='Markdown')

def editBoundQueueNumberNorth(queueNum):
    commonRegexRules = "^ZMOUT"
    msg = editBound(queueNum, commonRegexRules)
    return msg

@exception_handler
@logUserRecord
def CM_increaseQueueNumber(bot, update):
    logger = getLogger()

    userInfoLog = str(update.effective_message.chat)
    logger.debug(userInfoLog)

    msg = increaseQueueNumber()
    update.message.reply_text(msg, parse_mode='Markdown')


@exception_handler
@logUserRecord
def CM_resumeQueueNumber(bot, update):
    logger = getLogger()

    userInfoLog = str(update.effective_message.chat)
    logger.debug(userInfoLog)

    msg = resumeQueueNumber()
    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_getQueueList(bot, update):
    loginRCS()
    shippingHoleService = Web_RCS.ShippingSpaceService()
    response = shippingHoleService.sendJSON()

    dataList = json.loads(response.text)["data"]
    msg = ""
    for data in dataList:
        msg += "{}: {} ({})\n".format(data["spaceText"], data["queueMax"], data["statusStr"])

    update.message.reply_text(msg, parse_mode='Markdown')

def getCurrentQueueSetFromRCS():
    inverseBoundArea = INVERSE_BOUND_AREA  # from CONSTANT
    loginRCS()
    shippingHoleService = Web_RCS.ShippingSpaceService()
    response = shippingHoleService.sendJSON()

    dataList = json.loads(response.text)["data"]

    areaBoundDict = {}

    for data in dataList:
        if data["spaceText"] not in inverseBoundArea.keys():
            continue
        area = inverseBoundArea[data["spaceText"]]
        if area not in areaBoundDict.keys():
            areaBoundDict[area] = {}

        areaBoundDict[area][data["spaceText"]] = (
        {"spaceText": data["spaceText"], "queueMax": data["queueMax"], "statusStr": data["statusStr"]})


def getShippingSpaceMsg(dataList):
    inverseBoundArea = INVERSE_BOUND_AREA # from CONSTANT

    areaBoundDict = {}


    msg = ""
    for data in dataList:
        if data["spaceText"] not in inverseBoundArea.keys():
            continue
        area = inverseBoundArea[data["spaceText"]]
        if area not in areaBoundDict.keys():
            areaBoundDict[area] = {}

        areaBoundDict[area][data["spaceText"]] = (
        {"spaceText": data["spaceText"], "queueMax": data["queueMax"], "statusStr": data["statusStr"]})

    for area, boundDictDict in areaBoundDict.items():
        boundNameList = [values["spaceText"] for values in boundDictDict.values()]
        boundNameList = sorted(boundNameList)
        msg += "{}:\n".format(area)
        for boundName in boundNameList:
            bound = boundDictDict[boundName]
            msg += "{}: {} ({})\n".format(bound["spaceText"], bound["queueMax"], bound["statusStr"])
        msg += "\n"

    return msg

@exception_handler
@logUserRecord
def CM_getQueueStatus(bot, update):
    loginRCS()
    shippingHoleService = Web_RCS.ShippingSpaceService()
    response = shippingHoleService.sendJSON()

    dataList = json.loads(response.text)["data"]

    msg = "{}\n\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    msg += getShippingSpaceMsg(dataList)
    update.message.reply_text(msg, parse_mode='Markdown')


@exception_handler
@logUserRecord
def CM_editQueueNum(bot, update):
    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-2:]

    commonRegexRules = clearedInputText[0]
    queueNum = clearedInputText[1]

    msg = editBound(queueNum, commonRegexRules)

    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_editQueueOpen(bot, update):
    loginRCS()
    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[-2:]

    commonRegexRules = clearedInputText[0]
    openClose = clearedInputText[1]

    openCloseInput = 1
    # <=0 == close,   >0 --> open
    if int(openClose) <= 0:
        openCloseInput = 0

    msg = editBondOpenClose(openCloseInput, rules=commonRegexRules)

    update.message.reply_text(msg, parse_mode='Markdown')

# #createQueueSet Name
# deleteQueueSet Name
#
# showQueueSet
# showQueueSetStatus --> A time Active
#
#
# editQueueSet A MOUT01 3
#
# deployQueueSet 1200 1400 A
# stopQueueSet 1200 1400 A

# dict data Structure
#
a = {"A": {"deployStatus": {"status": "open", "timeslot": {"start": 1200, "end": 1200}}, "queueDict": {"MOUT01": {"queueNum": 3, "statusStr": "open"}}}}


# pastPickleDict[setName] = {"queueDict": queueDict,
#                                "deployStatus": {"status": "stopped", "timeslot": {"start": None, "end": None}},
#                                "isDefault": isSetDefault}

def _getDefaultQueueSetNameList(queueSetEditDict):
    queueDict = {}
    defaultQueueNameList = []
    for queueName, queueInfoDict in queueSetEditDict.items():
        if queueInfoDict["isDefault"]:
            defaultQueueNameList.append(queueName)

    return defaultQueueNameList


def _getQueueDictByArea(queueDict):

    inverseBoundAreaDict = INVERSE_BOUND_AREA

    areaBoundDict = {}

    for boundName, boundDict in queueDict.items():
        if boundName not in inverseBoundAreaDict.keys():
            continue
        belongedArea = inverseBoundAreaDict[boundName]
        if belongedArea not in areaBoundDict.keys():
            areaBoundDict[belongedArea] = {}

        areaBoundDict[belongedArea][boundName] = boundDict

    # sort
    tempSortDict = {area: areaBoundDict[area].keys() for area in areaBoundDict.keys()}

    for area in tempSortDict.keys():
        tempSortDict[area] = sorted(list(tempSortDict[area]))

    copyAreaBoundDict = copy.deepcopy(areaBoundDict)

    for area, sortedNameList in tempSortDict.items():
        copyAreaBoundDict[area] = {}
        for locationName in sortedNameList:
            areaDict = copyAreaBoundDict[area]
            areaDict[locationName] = areaBoundDict[area][locationName]


    return copyAreaBoundDict


@exception_handler
@logUserRecord
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

    pastPickleDict = getQueueSetFromPickle(fileName)

    if setName in pastPickleDict.keys():
        msg = "{} already set".format(setName)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg


    try:
        loginRCS()
        shippingSpaceService = Web_RCS.ShippingSpaceService()
        queueList = json.loads(shippingSpaceService.sendJSON().text)["data"]
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

    isSetDefault = False

    if not pastPickleDict.keys(): # is it first queueSet
        isSetDefault = True

    pastPickleDict[setName] = {"queueDict": queueDict,
                               "deployStatus": {"status": False, "timeslot": {"start": None, "end": None}},
                               "isDefault": isSetDefault}



    saveQueueSetToPickle(pastPickleDict, fileName)



    msg = getDeployStatusMsg()

    update.message.reply_text(msg, parse_mode='Markdown')

@exception_handler
@logUserRecord
def CM_setDefaultQueueSet(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()
    inputList = []
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    targetQueueSetName = inputText.split(" ")[-1]

    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = "{}\n".format(datetime.datetime.now())

    if targetQueueSetName not in pastPickleDict.keys():
        msg += "{} is not existed".format(targetQueueSetName)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg

    pastDefaultSetName = ""

    for queueSetName, queueSetDict in pastPickleDict.items():
        if queueSetDict["isDefault"]:
            pastDefaultSetName += "\t{}".format(queueSetName)
            pastPickleDict[queueSetName]["isDefault"] = False


    pastPickleDict[targetQueueSetName]["isDefault"] = True

    saveQueueSetToPickle(pastPickleDict, fileName)

    if pastDefaultSetName:
        msg += "({}) to {} (Default) ".format(pastDefaultSetName, targetQueueSetName)
    else:
        msg += "{} (Default)".format(targetQueueSetName)

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg

@exception_handler
@logUserRecord
def CM_cancelQueueSetDefault(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()

    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    targetDeleteQueueSet = inputText.split(" ")[-1]


    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = "{}\n".format(datetime.datetime.now())

    if targetDeleteQueueSet not in pastPickleDict.keys():
        msg += "{} is not existed (cancel Action Failed) ".format(targetDeleteQueueSet)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg


    # check whether target delete set is default Queue Set

    supplementaryMsg = ""

    pastPickleDict[targetDeleteQueueSet]["isDefault"] = False

    saveQueueSetToPickle(pastPickleDict, fileName)

    msg += "{} default is set to False \n".format(targetDeleteQueueSet)
    msg += supplementaryMsg

    msg += "\n"
    msg += getDeployStatusMsg()

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg

@exception_handler
@logUserRecord
def CM_copyQueueSet(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()

    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    inputList = inputText.split(" ")[-2:]

    srcQueueSet = inputList[0]
    targetQueueSet = inputList[1]

    print(srcQueueSet, targetQueueSet)

    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = "{}\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    if srcQueueSet not in pastPickleDict.keys():
        msg += "{} is not existed".format(srcQueueSet)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg

    if targetQueueSet in pastPickleDict.keys():
        msg += "{} is already existed".format(srcQueueSet)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg

    pastPickleDict[targetQueueSet] = copy.deepcopy(pastPickleDict[srcQueueSet])
    pastPickleDict[targetQueueSet]["isDefault"] = False
    pastPickleDict[targetQueueSet]["deployStatus"]["status"] = False
    pastPickleDict[targetQueueSet]["deployStatus"]["timeslot"]["start"] = None
    pastPickleDict[targetQueueSet]["deployStatus"]["timeslot"]["end"] = None

    saveQueueSetToPickle(pastPickleDict, fileName)

    msg += "{} is created".format(targetQueueSet)

    msg += "\n\n"
    msg += getDeployStatusMsg()

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg


@exception_handler
@logUserRecord
def CM_deleteQueueSet(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()

    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    targetDeleteQueueSet = inputText.split(" ")[-1]


    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = "{}\n".format(datetime.datetime.now())

    if targetDeleteQueueSet not in pastPickleDict.keys():
        msg += "{} is not existed (Delete Action Failed) ".format(targetDeleteQueueSet)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg


    # check whether target delete set is default Queue Set

    supplementaryMsg = ""

    deletedTargetIsDefault = pastPickleDict[targetDeleteQueueSet]["isDefault"]

    del pastPickleDict[targetDeleteQueueSet]

    if deletedTargetIsDefault and len(pastPickleDict) > 1:
        selectedDefaultSetName = list(pastPickleDict.keys())[0]
        pastPickleDict[selectedDefaultSetName]["isDefault"] = True
        supplementaryMsg += "{} is selected as new default set\n".format(selectedDefaultSetName)

    saveQueueSetToPickle(pastPickleDict, fileName)

    msg += "{} is deleted\n".format(targetDeleteQueueSet)
    msg += supplementaryMsg

    msg += "\n"
    msg += getDeployStatusMsg()

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg


def getQueueDictMsg(pastPickleDict, targetQueueName, defaultQueueName, differenceList):
    pass
    msg = ""
    format = """Area:
                    MOUT01: 3 (4) -- Open (Close)"""

    targetInfoDict = pastPickleDict[targetQueueName]
    defaultInfoDict = pastPickleDict[defaultQueueName]

    defaultQueueDict = defaultInfoDict["queueDict"]


    targetAreaQueueDictByArea = _getQueueDictByArea(targetInfoDict["queueDict"])

    for area, boundInfoDict in targetAreaQueueDictByArea.items():
        msg += "{}:\n".format(area)
        for boundName, boundDict in boundInfoDict.items():
            if boundName in differenceList:
                defaultLocationDict = defaultQueueDict[boundName]
                if int(boundDict["queueMax"]) == int(defaultLocationDict["queueMax"]):
                    numMsg = "{}".format(boundDict["queueMax"])
                else:
                    numMsg = "{} ({})".format(boundDict["queueMax"], defaultLocationDict["queueMax"])

                if boundDict["statusStr"] == defaultLocationDict["statusStr"]:
                    statusMsg = "{}".format(boundDict["statusStr"])
                else:
                    statusMsg = "{} ({})".format(boundDict["statusStr"], defaultLocationDict["statusStr"])

                msg += "\t {}: {} | {}\n".format(boundName, numMsg, statusMsg)
                # msg += "\t{}: {} ({}) | {} ({})\n".format(boundName, boundDict["queueMax"], defaultLocationDict["queueMax"], boundDict["statusStr"], defaultLocationDict["statusStr"])
            else:
                msg += "\t{}: {} | {}\n".format(boundName, boundDict["queueMax"], boundDict["statusStr"])
        msg += "\n"
    return msg



@exception_handler
@logUserRecord
def CM_showQueueSet(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()

    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    targetQueueName = inputText.split(" ")[-1]

    pastPickleDict = getQueueSetFromPickle(fileName)

    defaultNameList = _getDefaultQueueSetNameList(pastPickleDict)

    msg = ""

    if targetQueueName not in pastPickleDict.keys():
        msg += "({}) is not created yet".format(targetQueueName)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg

    if len(defaultNameList) > 1:
        msg += "Error -- Too Many Default ({})".format(",".join(defaultNameList))
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg

    defaultName = defaultNameList[0]

    # pastPickleDict[setName] = {"queueDict": queueDict,
    #                            "deployStatus": {"status": "stopped", "timeslot": {"start": None, "end": None}},
    #                            "isDefault": isSetDefault}

    targetInfoDict = pastPickleDict[targetQueueName]
    defaultInfoDict = pastPickleDict[defaultName]
    defaultQueueDict = defaultInfoDict["queueDict"]

    queueDifferenceList = []


    for locationName, targetLocationDict in targetInfoDict["queueDict"].items():

        if locationName not in defaultQueueDict.keys():
            continue

        defaultLocationDict = defaultQueueDict[locationName]
        # "queueDict": {"MOUT01": {"queueNum": 3, "statusStr": "open"}}}\

        if targetLocationDict != defaultLocationDict:
            queueDifferenceList.append(locationName)

    msg += getQueueDictMsg(pastPickleDict, targetQueueName, defaultName, queueDifferenceList)

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg






def getDeployStatusMsg():
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = "{}\n\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    # sort show dict
    showPickleDict = {queueSetName: queueSetDict["deployStatus"]["timeslot"]["start"] for queueSetName, queueSetDict in pastPickleDict.items() } # startTime
    for queueSetName, queueValue in showPickleDict.items():
        if not queueValue:
            showPickleDict[queueSetName] = "0000"
    tempDict = {k: v for k, v in sorted(showPickleDict.items(), key=lambda item: item[1])}

    showPickleDict2 = {queueSetName: pastPickleDict[queueSetName] for queueSetName in tempDict.keys()}

    for queueSetName, queueDict in showPickleDict2.items():
        deployStatusDict = queueDict["deployStatus"]
        isDefault = queueDict["isDefault"]

        deployedStr = "Deployed" if deployStatusDict["status"] else "Stopped"

        msg += "{}:\n" \
               "    [{}]\n" \
               "Timeslot: ({} to {}) (Default: {}) \n\n".format(queueSetName, deployedStr,
                                                                     deployStatusDict["timeslot"]["start"], deployStatusDict["timeslot"]["end"],
                                                                     isDefault)

    return msg


@exception_handler
@logUserRecord
def CM_showQueueSetDeployStatus(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()

    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = getDeployStatusMsg()

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg


@exception_handler
@logUserRecord
def CM_editQueueSet(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()

    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    targetParamsList = inputText.split(" ")[1:]
    targetQueueName = targetParamsList[0]

    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = "{}\n\n".format(str(datetime.datetime.now().strftime(DATETIME_FORMAT)))

    if targetQueueName not in pastPickleDict.keys():
        msg += "({}) is not created yet".format(targetQueueName)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg

    # transfer input into dict
    stationInputList = targetParamsList[1:]

    # if len(stationInputList) % 2:
    #     msg += "Input params should be in pairs: {}".format(str(stationInputList))
    #     update.message.reply_text(msg, parse_mode='Markdown')
    #     return msg


    editStationDict = {}

    totalNumOfInputSet = len(stationInputList)/3

    for i in range(0, len(stationInputList), 3):
        stationName = stationInputList[i]
        stationQueueNum = int(stationInputList[i+1])
        openOrClose = int(stationInputList[i+2])

        if stationName not in editStationDict.keys():
            editStationDict[stationName] = {"queueMax": 3, "statusStr": "Close"}
        statusStr = "Open" if openOrClose else "Close"
        editStationDict[stationName] = {"queueMax": stationQueueNum, "statusStr": statusStr}

    targetQueueSet = pastPickleDict[targetQueueName]

    targetQueueDict = targetQueueSet["queueDict"]

    msg += "{}:\n\n".format(targetQueueName)

    for editStationName, editQueueDict in editStationDict.items():
        if editStationName not in targetQueueDict.keys():
            continue
        msg += "{}: {} to {}\n".format(editStationName, targetQueueDict[editStationName], editQueueDict)
        print(editStationName, editQueueDict)
        targetQueueDict[editStationName] = editQueueDict



    saveQueueSetToPickle(pastPickleDict, fileName)
    update.message.reply_text(msg, parse_mode='Markdown')
    return msg


@exception_handler
@logUserRecord
def CM_deployQueueSet(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()

    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    targetParamsList = inputText.split(" ")[1:]
    targetQueueName = targetParamsList[0]
    deployOrStopped = int(targetParamsList[1])

    queueSetTimeDict = {}



    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = "{}\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    if targetQueueName not in pastPickleDict.keys():
        msg += "({}) is not created yet".format(targetQueueName)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg


    if deployOrStopped:
        pastPickleDict[targetQueueName]["deployStatus"]["status"] = True
    else:
        pastPickleDict[targetQueueName]["deployStatus"]["status"] = False


    if deployOrStopped and len(targetParamsList) == 4:
        startTime = targetParamsList[2]
        endTime = targetParamsList[3]

        timeSlotDict = pastPickleDict[targetQueueName]["deployStatus"]["timeslot"]

        if int(startTime) < 0 or int(startTime) > 2400 or int(endTime) < 0 or int(endTime) > 2400:
            msg += "{} {} timeslot error".format(startTime, endTime)
            update.message.reply_text(msg, parse_mode='Markdown')
            return msg

        timeSlotDict["start"] = startTime
        timeSlotDict["end"] = endTime


    saveQueueSetToPickle(pastPickleDict, fileName)

    print("")
    # handled msg send task
    msg = getDeployStatusMsg()
    update.message.reply_text(msg, parse_mode='Markdown')
    return msg

    # CM_showQueueSetDeployStatus(bot, update)

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
@logUserRecord
def CM_updateQueueSetToRCS(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    logger = getLogger()

    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    targetParamsList = inputText.split(" ")[1:]
    targetQueueName = targetParamsList[0]


    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = "{}\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    if targetQueueName not in pastPickleDict.keys():
        msg += "({}) is not created yet".format(targetQueueName)
        update.message.reply_text(msg, parse_mode='Markdown')
        return msg

    changeQueueSetToRCS(pastPickleDict[targetQueueName]["queueDict"])

    msg = CM_getQueueStatus(bot, update)
    print("CM_updateQueueSetToRCS")
    return msg

    # CM_showQueueSetDeployStatus(bot, update)

@exception_handler
@logUserRecord
def CM_error(bot, update):
    msg = "hi"
    update.message.reply_text(msg, parse_mode='Markdown')
    a = 0
    b = 1
    c = b/a
    return msg

def updateQueueSetToRCS(targetQueueName):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["queueSetEdit"]
    pastPickleDict = getQueueSetFromPickle(fileName)

    msg = "{}\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    if targetQueueName not in pastPickleDict.keys():
        msg += "({}) is not created yet".format(targetQueueName)
        return msg

    changeQueueSetToRCS(pastPickleDict[targetQueueName]["queueDict"])

def deployQueueSet(bot, update):
    pass

def stopQueueSet(bot, update):
    pass



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


@exception_handler
@logUserRecord
@logUserRecord
def CM_subscribeQueueNotification(bot, update):
    SUBSCIRPTION_DICT = {"queueChangeNotification": "queueChangeNotification.pkl",
                         "stagingChangeNotification": "stagingChangeNotification.pkl",
                         "stationChangeNotification": "stationChangeNotification.pkl"}
    fileName = RCS_CONSTANT.SUBSCIRPTION_DICT["queueChangeNotification"]
    subscriptionList = getSubscriptionListFromPickle(fileName)

    userID = update.callback_query.message.chat.id

    msg = "{}\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    if userID not in subscriptionList:
        subscriptionList.append(userID)
        msg += "{} is added to queue notification list".format(userID)
    else:
        subscriptionList.remove(userID)
        msg += "{} is removed from queue notification list".format(userID)

    saveSubscriptionListToPickle(subscriptionList, fileName)

    return msg

@exception_handler
@logUserRecord
def CM_stagingQueueNotification(bot, update):

    fileName = RCS_CONSTANT.SUBSCIRPTION_DICT["stagingChangeNotification"]
    subscriptionList = getSubscriptionListFromPickle(fileName)

    userID = update.callback_query.message.chat.id

    msg = "{}\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    if userID not in subscriptionList:
        subscriptionList.append(userID)
        msg += "{} is added to queue notification list".format(userID)
    else:
        subscriptionList.remove(userID)
        msg += "{} is removed from queue notification list".format(userID)

    saveSubscriptionListToPickle(subscriptionList, fileName)

    return msg

@exception_handler
@logUserRecord
def CM_getMyNotificationList(bot, update):

    msg = "{}\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    userID = update.callback_query.message.chat.id

    msg += "{}\n".format(userID)
    for notificationName, fileName in RCS_CONSTANT.SUBSCIRPTION_DICT.items():
        subscriptionList = getSubscriptionListFromPickle(fileName)

        if userID not in subscriptionList:
            msg += "{}\n".format(notificationName)

    return msg



@exception_handler
@logUserRecord
def CM_sendMsgToSubscriptionList(bot, update):
    SUBSCIRPTION_DICT = {"queueChangeNotification": "queueChangeNotification.pkl",
                         "stagingChangeNotification": "stagingChangeNotification.pkl",
                         "stationChangeNotification": "stationChangeNotification.pkl"}

    fileName = RCS_CONSTANT.SUBSCIRPTION_DICT["queueChangeNotification"]
    subscriptionList = getSubscriptionListFromPickle(fileName)

    # userID = update.callback_query.message.chat.id

    msg = "hello Testing"

    for chat_id in subscriptionList:
        bot.send_message(chat_id, msg)

    # return msg

@exception_handler
@logUserRecord
def CM_getStagingNumMon(bot, update):
    fileName = RCS_CONSTANT.ROUTE_FILENAME_DICT["stagingNumMonitor"]
    stagingDict = getStagingNumMonitorDictFromPickle(fileName)

    msg = "{}\n".format(datetime.datetime.now().strftime(DATETIME_FORMAT))

    for taskId, monitInfo in stagingDict.items():
        print( monitInfo["queueSetName"], monitInfo["targetStagingNum"])
        msg += "{}:\n queueSetName: {}\n targetStagingNum: {}\n\n".format(taskId, monitInfo["queueSetName"], monitInfo["targetStagingNum"])

    update.message.reply_text(msg, parse_mode='Markdown')
    return msg

@exception_handler
@logUserRecord
def CM_getLog(bot, update):
    try:
        msg = "{}\n".format(datetime.datetime.now())
        logger = getLogger()
        logFileName = logger.handlers[0].baseFilename
        msg += "{}\n".format(logFileName)
        with open(logFileName, "r+") as file:
            line = file.read()
            msg += line

        handleMsg(bot, update, msg)
        return msg

    except Exception as e:
        msg += str(e)
        handleMsg(bot, update, msg)

@exception_handler
@logUserRecord
def CM_getRouteLog(bot, update):
    try:
        msg = "{}\n".format(datetime.datetime.now())
        logger = getRouteLogger()
        logFileName = logger.handlers[0].baseFilename
        msg += "{}\n".format(logFileName)
        with open(logFileName, "r+") as file:
            line = file.read()
            msg += line

        handleMsg(bot, update, msg)
        return msg

    except Exception as e:
        msg += str(e)
        handleMsg(bot, update, msg)

@exception_handler
@logUserRecord
def CM_excludeAGV(bot, update):
    loginService = Web_RCS.LoginService()
    loginService.runService()

    excludeAGVService = Web_RCS.ExcludeAGVService()
    inputText = update.message.text
    agvNumList = inputText.split(" ")[1:]
    # agvNumList = targetParamsList[0]

    msg = "{}\n".format(datetime.datetime.now())

    for agvNum in agvNumList:
        excludeAGVService.excludeAGV(agvNum)
        result = excludeAGVService.sendJSON()
        msg += "{}\n".format(result.text)

    handleMsg(bot, update, msg)
    return msg

@exception_handler
@logUserRecord
def CM_cancelExcludeAGV(bot, update):
    loginService = Web_RCS.LoginService()
    loginService.runService()

    excludeAGVService = Web_RCS.ExcludeAGVService()
    inputText = update.message.text
    agvNumList = inputText.split(" ")[1:]
    # agvNumList = targetParamsList[0]

    msg = "{}\n".format(datetime.datetime.now())

    for agvNum in agvNumList:
        excludeAGVService.cancelExcludeAGV(agvNum)
        result = excludeAGVService.sendJSON()
        msg += "{}\n".format(result.text)

    handleMsg(bot, update, msg)
    return msg

@exception_handler
@logUserRecord
def CM_stopAGV(bot, update):
    loginService = Web_RCS.LoginService()
    loginService.runService()

    resumeStopAGVService = Web_RCS.ResumePauseAGVService()
    inputText = update.message.text
    agvNumList = inputText.split(" ")[1:]
    # agvNumList = targetParamsList[0]

    msg = "{}\n".format(datetime.datetime.now())

    for agvNum in agvNumList:
        resumeStopAGVService.stopAGV(agvNum)
        result = resumeStopAGVService.sendJSON()
        msg += "{}\n".format(result.text)

    handleMsg(bot, update, msg)
    return msg



@exception_handler
@logUserRecord
def CM_resumeAGV(bot, update):
    loginService = Web_RCS.LoginService()
    loginService.runService()

    resumeStopAGVService = Web_RCS.ResumePauseAGVService()
    inputText = update.message.text
    agvNumList = inputText.split(" ")[1:]
    # agvNumList = targetParamsList[0]

    msg = "{}\n".format(datetime.datetime.now())

    for agvNum in agvNumList:
        resumeStopAGVService.resumeAGV(agvNum)
        result = resumeStopAGVService.sendJSON()
        msg += "{}\n".format(result.text)

    handleMsg(bot, update, msg)
    return msg

@exception_handler
@logUserRecord
def CM_lowerBattery(bot, update):
    loginService = Web_RCS.LoginService()
    loginService.runService()

    lowerBatteryService = LowerBatteryService()
    inputText = update.message.text
    agvNumList = inputText.split(" ")[1:]
    # agvNumList = targetParamsList[0]

    ipDict = {}

    agvStatus = Web_RCS.AGVStatusService()
    for agvNum in agvNumList:
        agvStatus.selectAGV(agvNum)
        result = agvStatus.sendJSON()
        agvStatusDict = json.loads(result.text)["data"][0]
        ip = agvStatusDict["robotIp"]
        ipDict[agvNum] = ip

    msg = "{}\n".format(datetime.datetime.now())

    for agvNum, ip in ipDict.items():
        lowerBatteryService.setAGVIP(ip).setLowerBattery()
        result = lowerBatteryService.sendJSON()

        agvStatus.selectAGV(agvNum)
        result = agvStatus.sendJSON()
        agvStatusDict = json.loads(result.text)["data"][0]

        msg += "{} ({}): {}\n".format(agvNum, ip, str(agvStatusDict))

    handleMsg(bot, update, msg)
    return msg

@exception_handler
@logUserRecord
def CM_resumeBattery(bot, update):
    loginService = Web_RCS.LoginService()
    loginService.runService()

    lowerBatteryService = LowerBatteryService()
    inputText = update.message.text
    agvNumList = inputText.split(" ")[1:]
    # agvNumList = targetParamsList[0]

    ipDict = {}

    agvStatus = Web_RCS.AGVStatusService()
    for agvNum in agvNumList:
        agvStatus.selectAGV(agvNum)
        result = agvStatus.sendJSON()
        agvStatusDict = json.loads(result.text)["data"][0]
        ip = agvStatusDict["robotIp"]
        ipDict[agvNum] = ip

    msg = "{}\n".format(datetime.datetime.now())

    for agvNum, ip in ipDict.items():
        lowerBatteryService.setAGVIP(ip).resumeNormalBattery()
        result = lowerBatteryService.sendJSON()

        agvStatus.selectAGV(agvNum)
        result = agvStatus.sendJSON()
        agvStatusDict = json.loads(result.text)["data"][0]

        msg += "{} ({}): {}\n".format(agvNum, ip, str(agvStatusDict))

    handleMsg(bot, update, msg)
    return msg

@exception_handler
@logUserRecord
def CM_getAGVStatus(bot, update):
    loginService = Web_RCS.LoginService()
    loginService.runService()

    agvStatus = Web_RCS.AGVStatusService()

    lowerBatteryService = LowerBatteryService()
    inputText = update.message.text
    agvNumList = inputText.split(" ")[1:]

    msg = "{}\n".format(datetime.datetime.now())

    for agvNum in agvNumList:
        agvStatus.selectAGV(agvNum)
        result = agvStatus.sendJSON()
        agvStatusDict = json.loads(result.text)["data"][0]
        statusStr = ""
        for key, value in agvStatusDict.items():
            statusStr += "\t{}: {}\n".format(key, value)
        msg += "{}:\n {}\n\n".format(agvNum, str(statusStr))

    handleMsg(bot, update, msg)
    return msg


def getErrorSendingList(startTimeStr, endTimeStr):
    loginService = Web_RCS.LoginService()
    loginService.runService()

    taskSentMessageService = Web_RCS.TaskSentMessageService()
    taskSentMessageService.setEndTimeFrom(startTimeStr).setEndTimeTo(endTimeStr)
    taskSentMessageService.setSendStatus("Error sending")

    response = taskSentMessageService.sendJSON()
    dataList = json.loads(response.text)["data"]

    taskSentMessageService.setSendStatus("Sending")
    response = taskSentMessageService.sendJSON()
    sendingDataList = json.loads(response.text)["data"]

    return dataList + sendingDataList


@exception_handler
@logUserRecord
def CM_getErrorSending(bot, update):
    endTime = datetime.datetime.now()
    startTime = endTime - datetime.timedelta(days=1)

    startTimeStr = startTime.strftime(DATETIME_FORMAT)
    endTimeSTr = endTime.strftime(DATETIME_FORMAT)

    dataList = getErrorSendingList(startTimeStr, endTimeSTr)

    msg = "{}\n".format(endTimeSTr)

    for i in range(len(dataList)-1, -1, -1):
        data = dataList[i]
        msg += "dateCr: {}\n dateChg: {}\n rcptStatusStr: {}\n reqMsg: {}\n reqTypStr: {}\n sendMsg: {}\n taskCode:{}\n\n\n".format(
            data["dateCr"], data["dateChg"], data["rcptStatusStr"], data["reqMsg"], data["reqTypStr"], data["sendMsg"], data["taskCode"]
        )

    handleMsg(bot, update, msg)
    return msg

def getOnlineAGVDictList(agvStr):
    deviceStatusQueryService = Web_RCS.DeviceStatusQueryService()
    deviceStatusQueryService.setMapShortName("PnS")
    if agvStr == "-1" or agvStr == -1:
        deviceStatusQueryService.setRobotCode(agvStr)
    else:
        deviceStatusQueryService.setRobotList(agvStr)
    result = json.loads(deviceStatusQueryService.sendJSON().text)
    agvCloseList = result["data"]
    return agvCloseList

@exception_handler
@logUserRecord
def CM_getOnlineAGVDictList(bot, update):
    msg = "{}:\n".format(datetime.datetime.now())
    logger = getLogger()

    loginService = Web_RCS.LoginService()
    loginService.runService()

    agvListService = Web_RCS.AGVListService()
    agvListResult = json.loads(agvListService.sendJSON().text)
    totalNumberOfAGV = len(agvListResult["data"])


    agvCloseList = getOnlineAGVDictList("-1") # all agv
    print("")

    numberOfActiveAGV = len(agvCloseList)

    if numberOfActiveAGV/totalNumberOfAGV > 0.1:
        msg += "{}/{} : AGV percentage is not low enough to activate function".format(numberOfActiveAGV, totalNumberOfAGV)
        handleMsg(bot, update, msg)
        return msg

    # agvCloseList = getOnlineAGVDictList(",".join(agvCloseList)) # all agv
    keyList = ["robotCode", "robotIp", "battery", "statusStr", "excludeStr", "taskCode", "posX", "posY"]

    # shutDownAGVService = ShutDownAGVService()

    for agvDict in agvCloseList:
        for key in keyList:
            if key not in agvDict.keys():
                continue
            msg += "{}: {}\t".format(key, agvDict[key])
        msg += "\n"

    handleMsg(bot, update, msg)
    return msg


@exception_handler
@logUserRecord
def CM_haltAGV(bot, update):
    msg = "{}:\n".format(datetime.datetime.now())

    logger = getLogger()
    inputText = update.message.text

    userInfoLog = str(update.effective_message.chat)
    loggingMsg = "{}\n{}".format(inputText, userInfoLog)
    logger.debug(loggingMsg)

    clearedInputText = inputText.split(" ")[1:]

    agvCloseList = clearedInputText

    shutDownAGVService = ShutDownAGVService()

    loginService = Web_RCS.LoginService()
    loginService.runService()

    print(",".join(agvCloseList))
    agvOnlineCloseList = getOnlineAGVDictList(",".join(agvCloseList)) # all agv
    keyList = ["robotCode", "robotIp", "battery", "statusStr", "excludeStr", "taskCode", "posX", "posY"]

    for agvDict in agvOnlineCloseList:
        for key in keyList:
            if key not in agvDict.keys():
                continue
            msg += "{}: {}\t".format(key, agvDict[key])
        msg += "\n"
        shutDownAGVService.setAGVIP(agvDict["robotIp"]).shutdownAGV()
        result = shutDownAGVService.sendJSON()

    agvCloseList = getOnlineAGVDictList(",".join(agvCloseList)) # all agv
    keyList = ["robotCode", "robotIp", "battery", "statusStr", "excludeStr", "taskCode", "posX", "posY"]

    for agvDict in agvCloseList:
        for key in keyList:
            if key not in agvDict.keys():
                continue
            msg += "{}: {}\t".format(key, agvDict[key])
        msg += "\n"


    update.message.reply_text(msg, parse_mode='Markdown')
    return msg

@exception_handler
@logUserRecord
def CM_haltRemainingAGV(bot, update):
    msg = "{}:\n".format(datetime.datetime.now())
    logger = getLogger()

    loginService = Web_RCS.LoginService()
    loginService.runService()

    agvListService = Web_RCS.AGVListService()
    agvListResult = json.loads(agvListService.sendJSON().text)
    totalNumberOfAGV = len(agvListResult["data"])


    agvCloseList = getOnlineAGVDictList("-1") # all agv
    print("")

    numberOfActiveAGV = len(agvCloseList)

    if numberOfActiveAGV/totalNumberOfAGV > 0.1:
        msg += "{}/{} : AGV percentage is not low enough to activate function".format(numberOfActiveAGV, totalNumberOfAGV)
        handleMsg(bot, update, msg)
        return msg

    # agvCloseList = getOnlineAGVDictList(",".join(agvCloseList)) # all agv
    keyList = ["robotCode", "robotIp", "battery", "statusStr", "excludeStr", "taskCode", "posX", "posY"]

    shutDownAGVService = ShutDownAGVService()

    for agvDict in agvCloseList:
        for key in keyList:
            if key not in agvDict.keys():
                continue
            msg += "{}: {}\t".format(key, agvDict[key])
        msg += "\n"
        shutDownAGVService.setAGVIP(agvDict["robotIp"]).shutdownAGV()
        # print("debug")
        result = shutDownAGVService.sendJSON()

    msg += "After closed AGV\n"
    agvCloseList = getOnlineAGVDictList(",".join(agvCloseList)) # all agv
    keyList = ["robotCode", "robotIp", "battery", "statusStr", "excludeStr", "taskCode", "posX", "posY"]

    for agvDict in agvCloseList:
        for key in keyList:
            if key not in agvDict.keys():
                continue
            msg += "{}: {}\t".format(key, agvDict[key])
        msg += "\n"


    # update.message.reply_text(msg, parse_mode='Markdown')
    handleMsg(bot, update, msg)
    return msg



if __name__ == "__main__":
    logger = getLogger()
    initTGHandler(updater)
    updater.dispatcher.add_handler(CallbackQueryHandler(getClickButtonData))
    updater.dispatcher.add_handler(RegexHandler("/morningStaging", CM_morningStaging))
    updater.dispatcher.add_handler(RegexHandler("/nightStaging", CM_nightStaging))

    # msg = CM_stationTaskDurationNight(0, 0)

    updater.start_polling()
    updater.idle()