from values import CONSTANT
import datetime

def determineInboundAreaByCallSign(callSign):
    for area, callSignList in CONSTANT.INBOUND_DIVIDE2.items():
        if callSign in callSignList:
            return area
    return "404"

def generateTimeIntervalList(startTime, endTime, interval) :
    # variable format
    # startTime --> datetime, endTime --> dateTime, interview --> timedelta
    timeIntervalList = []
    tempStartTime = startTime
    while tempStartTime < endTime:
        timeIntervalList.append(tempStartTime)
        tempStartTime += interval
    timeIntervalList.append(endTime)
    return timeIntervalList

def generateTimeIntervalDict(timeIntervalList):
    hourCountDict = {}
    for i in range(len(timeIntervalList) - 1):
        timeIntervalStr = timeIntervalList[i].strftime("%Y-%m-%d %H:%M:%S") + " to " + timeIntervalList[i + 1].strftime("%Y-%m-%d %H:%M:%S")
        hourCountDict[timeIntervalStr] = None
    return hourCountDict

def generateTimePointDict(timeIntervalList):
    hourCountDict = {}
    for i in range(len(timeIntervalList)):
        timeIntervalStr = timeIntervalList[i].strftime("%Y-%m-%d %H:%M:%S")
        hourCountDict[timeIntervalStr] = None
    return hourCountDict

def generateTimeIntervalDictByHour(dayBeforeOrAfter):
    # variable format
    # dayBeforeOrAfter --> int
    today = datetime.datetime.today()
    startTime = (today + datetime.timedelta(days=dayBeforeOrAfter)).replace(hour=0, minute=0, second=0)
    endTime = today
    timeIntervalList = generateTimeIntervalList(startTime, endTime, datetime.timedelta(minutes=60))
    return generateTimeIntervalDict(timeIntervalList)

def generateTimePointDictByHalfHour(dayBeforeOrAfter):
    # variable format
    # dayBeforeOrAfter --> int
    today = datetime.datetime.today()
    startTime = (today + datetime.timedelta(days=dayBeforeOrAfter)).replace(hour=0, minute=0, second=0)
    endTime = today
    timeIntervalList = generateTimeIntervalList(startTime, endTime, datetime.timedelta(minutes=30))
    return generateTimePointDict(timeIntervalList)

def RCSTimestampToDate(RCStimeStamp):
    RCStimeStamp = str(RCStimeStamp)
    timestamp = float("{}.{}".format(RCStimeStamp[0:10], RCStimeStamp[10:-1]))
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

def RCSTimestampToDateTime(RCStimeStamp):
    RCStimeStamp = str(RCStimeStamp)
    timestamp = float("{}.{}".format(RCStimeStamp[0:10], RCStimeStamp[10:-1]))
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def withInRange(data, start, end):
    return (data >= start and data < end)

def sortDict(targetDict, sortedTempDict):
    # sorting dictionary by sorted Key

    tempDict = {}
    tempDict2 = {}
    keyListList = _getAllKeyList(sortedTempDict)



def _getAllKeyList(target):
    tempTarget = target
    keyListList = []
    if isinstance(tempTarget, dict):
        keyList = list(tempTarget.keys())
        keyListList.append(keyList)
        for key in keyList:
            recusiveResult = _getAllKeyList(tempTarget[key])
            if recusiveResult:
                keyListList.extend(recusiveResult)
    return keyListList


def convertRGBNumberToCode(R, G, B):
    if not (isinstance(R,int) and isinstance(G,int) and isinstance(B,int)):
        raise Exception("RGB input must be integer")
    if not withInRange(R, 0, 256) or not withInRange(G, 0, 256) or not withInRange(B, 0, 256):
        raise Exception("RGB input is out of range")
    return '#%02x%02x%02x' % (R, G, B)

def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60),
        ('second',      1)
    ]

    strings=[]
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value , seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)

def seconds_format(seconds):
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('d',         60*60*24),
        ('h',        60*60),
        ('m',      60),
        ('s',      1)
    ]

    strings=[]
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value , seconds = divmod(seconds, period_seconds)
            # has_s = 's' if period_value > 1 else ''
            strings.append("%s%s" % (period_value, period_name))

    return ",".join(strings)

if __name__ == "__main__":
    a = {"a": {"c": 1, "d": 2}, "b": 1, "e":{"q":1, "e":6}}
    keyListList = _getAllKeyList(a)
    print(keyListList)