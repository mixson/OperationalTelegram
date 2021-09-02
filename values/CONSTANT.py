


# ------------------------
import os
import copy

APPLICATION_NAME = ""
FULLPATH_ENDINDEX = os.getcwd().index(APPLICATION_NAME) + APPLICATION_NAME.__len__()
APPLICATION_NAME_FULL_PATH = os.getcwd()[0:FULLPATH_ENDINDEX]


# RCS Server Networking
class RCS_CONSTANT():
    PROTOCOL = "http"
    IP = "10.39.64.28"
    PORT = "80"
    SUPPORT_PORT = "8994"
    SYSTEM = "rcs"


# Server Networking
MAIN_SERVER_PROTOCOL = "http"
MAIN_SERVER_IP = "10.39.64.28"
MAIN_SERVER_PORT = "80"
MAIN_SERVER_SYSTEM = "sensor"
MAIN_SERVER_SERVICE = "getSensorStatus"

# Control Board Networking
# OUTBOUND A
OUTBOUND_A_CONTROL_BOARD_NAME = "raspberryPi4_A"
OUTBOUND_A_CONTROL_BOARD_IP = ""  # wait to be filled
OUTBOUND_A_CONTROL_BOARD_PORT = "80"
OUTBOUND_A_CONTROL_BOARD_SYSTEM = "sensor"
OUTBOUND_A_CONTROL_BOARD_SERVICE = "getSensorStatus"

# Database Parameters A
OUTBOUND_A_DATABASE_PROTOCOL = "mongodb"
OUTBOUND_A_DATABASE_IP = "localhost"
OUTBOUND_A_DATABASE_PORT = "27017"

# sensor_parameter
DATA_INTERVAL = 2  # seconds

# Area Division
AREA_NAME = {"INBOUND": ["INBOUND_1", "INBOUND_2"],
             "FINGER": ["FINGER_1", "FINGER_2", "FINGER_3", "FINGER_4"],
             "OUTBOUND": ["OUTBOUND_1", "OUTBOUND_2"]
             }

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

INBOUND_DIVIDE = {"North_A": ["MIN01", "MIN02", "MIN03", "MIN04", "MIN05", "MIN06", "MIN07", "MIN22"],
                  "North_B": ["MIN08", "MIN09", "MIN10", "MIN11", "MIN12", "MIN13", "MIN14", "MIN15", "MIN21"],
                  "East": ["RMIN01", "RMIN02", "RMIN03", "RMIN04", "RMIN05", "RMIN06"],
                  "GTM": ["LMIN01", "LMIN02", "LMIN03"],
                  "West": ["LMIN04", "LMIN05", "LMIN06", "LMIN07", "LMIN08", "LMIN09", "LMIN10"]
                  }

INBOUND_DIVIDE2 = {"A": ["MIN01", "MIN02", "MIN03", "MIN04", "MIN05", "MIN06", "MIN07", "MIN08", "MIN09", "MIN10", "MIN22",],
                  "B": [ "MIN11", "MIN12", "MIN13", "MIN14", "MIN15", "MIN16", "MIN17", "MIN18", "MIN19", "MIN20", "MIN21"],
                  "E": ["RMIN01", "RMIN02", "RMIN03", "RMIN04", "RMIN05", "RMIN06"],
                  "GTM": ["LMIN01", "LMIN02", "LMIN03"],
                  "W": ["LMIN04", "LMIN05", "LMIN06", "LMIN07", "LMIN08", "LMIN09", "LMIN10"],
                   "S": ["NMIN01", "NMIN02", "NMIN03", "NMIN04",]
                  }
OUTBOUND_DIVIDE = {"A": ["MOUT01", "MOUT02", "MOUT04"],
                   "B": ["MOUT05", "MOUT06", "MOUT09","MOUT10","MOUT12"],
                   "E": ["RMIN01", "RMIN02", "RMIN03", "RMIN04", "RMIN05", "RMIN06"],
                   "GTM": ["ZMOUT01", "ZMOUT02", "ZMOUT03"],
                   "W": ["LMIN04", "LMIN05", "LMIN06", "LMIN07", "LMIN08", "LMIN09", "LMIN10"],
                   "S": ["NMOUT01", "NMOUT02", "NMOUT03", "NMOUT04", ]
                   }

BOUND_DIVIDE = copy.deepcopy(INBOUND_DIVIDE2)
for area, boundList in OUTBOUND_DIVIDE.items():
    BOUND_DIVIDE[area].extend(boundList)

INVERSE_BOUND_AREA = {}

for area, boundList in BOUND_DIVIDE.items():
    for bound in boundList:
        INVERSE_BOUND_AREA[bound] = area


WORKING_STATION_DIVIDE = {
    "FINGER_1": ["A101", "A102", "A103", "A104", "A105", "A106", "A107", "A108", "A109", "A110", "A111", "A112", "A129", "A130", "A131"],
    "FINGER_2": ["A113", "A114", "A115", "A116", "A117", "A118", "A119", "A120", "A121", "A122", "A123", "A124", "A125", "A126", "A127",
                 "A128", "A201", "A202", "A203", "A204", "A205", "A206", "A207", "A208", "A209", "A210", "A211", "A212", "A213", "A214", "A215",
                 "A216"],
    "FINGER_3": ["A217", "A218", "A219", "A220", "A221", "A222", "A223", "A224", "A225", "A226", "A227", "A228", "A229", "A230", "A231", "A232",
                 "A301", "A302", "A303", "A304", "A305", "A306", "A307", "A308", "A309", "A310", "A311", "A312", "A313", ],
    "FINGER_4": ["A314", "A315", "A316", "A317", "A318", "A319", "A320", "A321", "A322", "A323", "A324", "A325", "A326",
                 "A401", "A402", "A403", "A404", "A405", "A406", "A407", "A408", "A409", "A410", "A411", "A412", "A413", "A414", "A415"]}

STATION_QUEUE_NUM = {
    "A101": 3,
    "A102": 3,
    "A103": 4,
    "A104": 3,
    "A105": 3,
    "A106": 3,
    "A107": 3,
    "A108": 3,
    "A109": 3,
    "A110": 3,
    "A111": 3,
    "A112": 3,
    "A113": 3,
    "A114": 3,
    "A115": 3,
    "A116": 3,
    "A117": 3,
    "A118": 3,
    "A119": 3,
    "A120": 3,
    "A121": 3,
    "A122": 3,
    "A123": 3,
    "A124": 3,
    "A125": 3,
    "A126": 3,
    "A127": 3,
    "A128": 3,
    "A129": 3,
    "A130": 3,
    "A131": 3,

    "A201": 2,
    "A202": 2,
    "A203": 2,
    "A204": 2,
    "A205": 2,
    "A206": 2,
    "A207": 3,
    "A208": 2,
    "A209": 2,
    "A210": 2,
    "A211": 2,
    "A212": 2,
    "A213": 2,
    "A214": 2,
    "A215": 2,
    "A216": 3,

    "A217": 3,
    "A218": 3,
    "A219": 3,
    "A220": 3,
    "A221": 3,
    "A222": 3,
    "A223": 3,
    "A224": 3,
    "A225": 3,
    "A226": 3,
    "A227": 3,
    "A228": 3,
    "A229": 3,
    "A230": 3,
    "A231": 3,
    "A232": 3,
    "A301": 4,
    "A302": 4,
    "A303": 4,
    "A304": 4,
    "A305": 4,
    "A306": 3,
    "A307": 3,
    "A308": 4,
    "A309": 4,
    "A310": 4,
    "A311": 4,
    "A312": 6,
    "A313": 5,

    "A314": 5,
    "A315": 5,
    "A316": 5,
    "A317": 4,
    "A318": 4,
    "A319": 4,
    "A320": 3,
    "A321": 3,
    "A322": 4,
    "A323": 4,
    "A324": 4,
    "A325": 5,
    "A326": 6,
    "A401": 3,
    "A402": 3,
    "A403": 3,
    "A404": 3,
    "A405": 3,
    "A406": 3,
    "A407": 3,
    "A408": 3,
    "A409": 3,
    "A410": 3,
    "A411": 3,
    "A412": 3,
    "A413": 3,
    "A414": 3,
    "A415": 3,


}

COMBINED_STATION_DICT = {
                    "A101": "A102",
                    "A103": "A104",
                    "A105" : "A106",
                    "A107" : "A108",
                    "A109" : "A110",
                    "A111" : "A112",

                    "A113" : "A114",
                    "A115" : "A116",
                    "A117" : "A118",
                    "A119" : "A120",
                    "A121" : "A122",
                    "A123" : "A124",
                    "A125" : "A126",
                    "A127" : "A128",

                    "A201": "A202",
                    "A203" : "A204",
                    "A205" : "A206",
                    "A207" : "A208",
                    "A209" : "A210",
                    "A211" : "A212",
                    "A213" : "A214",
                    "A215" : "A216",

                    "A217": "A218",
                    "A219" : "A220",
                    "A221" : "A222",
                    "A223" : "A224",
                    "A225" : "A226",
                    "A227" : "A228",
                    "A229" : "A230",
                    "A231" : "A232",


                    "A301": "A302",
                    "A304" : "A305",
                    "A306" : "A307",
                    "A308" : "A309",
                    "A310" : "A311",
                    "A312" : "A313",

                    "A314": "A315",
                    "A317" : "A318",
                    "A319" : "A320",
                    "A321" : "A322",
                    "A323" : "A324",
                    "A325" : "A326",

                    "A402" : "A403",
                    "A404" : "A405",
                    "A406" : "A407",
                    "A408" : "A409",
                    "A410" : "A411",
                    "A412" : "A413",
                    "A414" : "A415",

                    }

SINGLE_STATION_LIST = ["A129", "A130","A131","A316","A303","A401",]

STATION_FINGER_AVERAGE_OVERWELMED_PERCENTAGE = {
    "FINGER_1_LEFT": float(1/19) * 100 * 1.2,
    "FINGER_1_RIGHT": float(1/19) * 100 * 1.2,
    "FINGER_2_LEFT": float(1/32) * 100 * 1.2,
    "FINGER_2_RIGHT": float(1/32) * 100 * 1.2,
    "FINGER_3_LEFT": float(1/29) * 100 * 1.2,
    "FINGER_3_RIGHT": float(1/29) * 100 * 1.2,
    "FINGER_4_LEFT": float(1/28) * 100 * 1.2,
    "FINGER_4_RIGHT": float(1/28) * 100 * 1.2
} # 1.2 mean over 20 percentage

STATION_OVERWHELMED_PERCENTAGE = {
    "FINGER_1_LEFT": {"A129":0.0, "A130":0.0, "A131":0.0},
    "FINGER_1_RIGHT": {"A101": 0.0, "A102": 0.0, "A103": 0.0, "A104": 0.0, "A105": 0.0, "A106": 0.0, "A107": 0.0, "A108": 0.0, "A109": 0.0, "A110": 0.0, "A111": 0.0, "A112": 0.0 },
    "FINGER_2_LEFT": {"A113":0.0, "A114":0.0, "A115":0.0, "A116":0.0, "A117":0.0, "A118":0.0, "A119":0.0, "A120":0.0, "A121":0.0, "A122":0.0, "A123":0.0, "A124":0.0, "A125":0.0, "A126":0.0, "A127":0.0, "A128":0.0},
    "FINGER_2_RIGHT": {"A201":0.0, "A202":0.0, "A203":0.0, "A204":0.0, "A205":0.0, "A206":0.0, "A207":0.0, "A208":0.0, "A209":0.0, "A210":0.0, "A211":0.0, "A212":0.0, "A213":0.0, "A214":0.0, "A215":0.0, "A216":0.0},
    "FINGER_3_LEFT": {"A217":0.0, "A218":0.0, "A219":0.0, "A220":0.0, "A221":0.0, "A222":0.0, "A223":0.0, "A224":0.0, "A225":0.0, "A226":0.0, "A227":0.0, "A228":0.0, "A229":0.0, "A230":0.0, "A231":0.0, "A232":0.0},
    "FINGER_3_RIGHT": {"A301":0.0, "A302":0.0, "A303":0.0, "A304":0.0, "A305":0.0, "A306":0.0, "A307":0.0, "A308":0.0, "A309":0.0, "A310":0.0, "A311":0.0, "A312":0.0, "A313":0.0 },
    "FINGER_4_LEFT": {"A314":0.0, "A315":0.0, "A316":0.0, "A317":0.0, "A318":0.0, "A319":0.0, "A320":0.0, "A321":0.0, "A322":0.0, "A323":0.0, "A324":0.0, "A325":0.0, "A326":0.0},
    "FINGER_4_RIGHT": {"A401":0.0, "A402":0.0, "A403":0.0, "A404":0.0, "A405":0.0, "A406":0.0, "A407":0.0, "A408":0.0, "A409":0.0, "A410":0.0, "A411":0.0, "A412":0.0, "A413":0.0, "A414":0.0, "A415": 0.0,}
}


for fingerName, stationDict in STATION_OVERWHELMED_PERCENTAGE.items():
    for stationName in stationDict.keys():
        STATION_OVERWHELMED_PERCENTAGE[fingerName][stationName] = STATION_FINGER_AVERAGE_OVERWELMED_PERCENTAGE[fingerName]

WORKING_STATION_COUNT = {}
WORKING_STATION_TOTAL_SUM = 0
WORKING_STATION_PERCENTAGE_BY_FINGER = {}
WORKING_STATION_PERCENTAGE_IN_FINGER = {}


# WORKING_STATION_COUNT
# WORKING_STATION_TOTAL_SUM
for fingerName, stationDict in STATION_OVERWHELMED_PERCENTAGE.items():
    for stationName in stationDict.keys():
        if fingerName not in WORKING_STATION_COUNT.keys():
            WORKING_STATION_COUNT[fingerName] = 0
        WORKING_STATION_COUNT[fingerName] += 1
        WORKING_STATION_TOTAL_SUM += 1

# WORKING_STATION_PERCENTAGE_BY_FINGER
for fingerName, stationDict in WORKING_STATION_COUNT.items():
            WORKING_STATION_PERCENTAGE_BY_FINGER[fingerName] = WORKING_STATION_COUNT[fingerName]/ WORKING_STATION_TOTAL_SUM * 100

# WORKING_STATION_PERCENTAGE_IN_FINGER
for fingerName, stationDict in STATION_OVERWHELMED_PERCENTAGE.items():
    for stationName in stationDict.keys():
        if fingerName not in WORKING_STATION_PERCENTAGE_IN_FINGER.keys():
            WORKING_STATION_PERCENTAGE_IN_FINGER[fingerName] = {}
        WORKING_STATION_PERCENTAGE_IN_FINGER[fingerName][stationName] = 1 / WORKING_STATION_COUNT[fingerName] * 100


storeMapping = {'A101': ['643', '160', '187', '403'],
                'A102': ['12', '66', '470'],
                'A103': ['255', '640', '634'],
                'A104': ['257', '670', '619'],
                'A105': ['79', '264', '435'],
                'A106': ['476'],
                'A107': ['491', '471', '409'],
                'A108': ['439', '31'],
                'A109': ['107', '424', '203'],
                'A110': ['48', '690'],
                'A111': ['697', '18', '56'],
                'A112': ['67', '24', '446', '132'],
                'A113': ['429', '226', '489', '222'],
                'A114': ['454', '478', '164'],
                'A115': ['681'],
                'A116': ['246', '259', '477'],
                'A117': ['285', '273', '463'],
                'A118': ['119', '687'],
                'A119': ['296', '623'],
                'A120': ['108', '476', '443'],
                'A121': ['189', '453'],
                'A122': ['109', '261'],
                'A123': ['262', '167', '11'],
                'A124': ['682', '136'],
                'A125': ['62', '465', '291'],
                'A126': ['162', '674'],
                'A127': ['195', '112'],
                'A128': ['277', '57', '496', '180'],
                'A129': ['468', '494', '904', '902', '461', '298', '282'],
                'A130': ['115', '10', '909', '906', '617', '228', '114', '199', '138'],
                'A131': ['127', '122', '616', '146', '933', '932', '930', '99', '85'],
                'A201': ['130', '154', '487', '96'],
                'A202': ['237', '466', '269'],
                'A203': ['133', '492'],
                'A204': ['219', '635', '422'],
                'A205': ['157', '141', '652'],
                'A206': ['631', '696'],
                'A207': ['188', '637'],
                'A208': ['191', '178', '280'],
                'A209': ['922', '275'],
                'A210': ['922', '144'],
                'A211': ['182', '695', '669'],
                'A212': ['77', '607'],
                'A213': ['45', '480'],
                'A214': ['922', '175', '644'],
                'A215': ['922', '207'],
                'A216': ['686', '111', '128', '421'],
                'A217': ['68', '169', '192', '98'],
                'A218': ['452', '451', '213'],
                'A219': ['659', '649'],
                'A220': ['655', '479', '485'],
                'A221': ['407', '256', '658'],
                'A222': ['278', '692'],
                'A223': ['229', '438'],
                'A224': ['495', '657', '161'],
                'A225': ['135', '665'],
                'A226': ['666', '159'],
                'A227': ['65', '137', '455'],
                'A228': ['268', '170'],
                'A229': ['38', '252'],
                'A230': ['688', '417', '694'],
                'A231': ['481', '685'],
                'A232': ['101', '206', '483', '672'],
                'A301': ['460', '431', '5'],
                'A302': ['148', '642', '464'],
                'A303': ['638', '208', '645'],
                'A304': ['201', '89', '691'],
                'A305': ['677'],
                'A306': ['153', '263', '639'],
                'A307': ['105', '497', '272', '618'],
                'A308': ['254', '636', '158'],
                'A309': ['258', '121'],
                'A310': ['288', '185', '150'],
                'A311': ['232', '473', '498'],
                'A312': ['662', '457', '661', '294'],
                'A313': ['92', '430', '299', '265'],
                'A314': ['490', '227', '699'],
                'A315': ['664', '74', '614'],
                'A316': ['147', '668', '123'],
                'A317': ['110', '646', '675'],
                'A318': ['41'],
                'A319': ['667', '131', '224'],
                'A320': ['458', '401', '650', '613'],
                'A321': ['462', '276', '260', '234'],
                'A322': ['689', '290'],
                'A323': ['271', '270'],
                'A324': ['602', '683', '293'],
                'A325': ['7', '605', '156', '671'],
                'A326': ['124', '30', '493', '27'],
                'A401': ['174', '484'],
                'A402': ['217', '274'],
                'A403': ['660', '287', '165'],
                'A404': ['103', '242'],
                'A405': ['151', '149', '647'],
                'A406': ['474', '651'],
                'A407': ['129', '145', '177'],
                'A408': ['678', '467'],
                'A409': ['116', '97'],
                'A410': ['183', '486', '78'],
                'A411': ['676', '253'],
                'A412': ['418', '412'],
                'A413': ['106', '456', '179'],
                'A414': ['248', '684'],
                'A415': ['427', '413']}

storeMapping_Count = {'FINGER_1': 59, 'FINGER_2': 83, 'FINGER_3': 81, 'FINGER_4': 74}
storeMapping_Percentage = {'FINGER_1': 20, 'FINGER_2': 28, 'FINGER_3': 27, 'FINGER_4': 25}

AREA_COORDINATION_DIVIDE = {"Left_1": {"x_0": 82420 - 300, "y_0": 46950 - 100, "x_1": 85640 - 141, "y_1": 54410 + 100}, #x 1
                            "Left_2": {"x_0": 82420 - 300, "y_0": 63640 - 100, "x_1": 85640 - 141, "y_1": 71060 + 100}, #x 2
                            "LeftTop_1": {"x_0": 82420 - 300, "y_0": 83400 + 1, "x_1": 124300 - 1, "y_1": 100000 + 100}, #x 3
                            "RightTop_2": {"x_0": 124300, "y_0": 83400 + 1, "x_1": 165723 - 1, "y_1": 100000 + 100}, #x 6
                            "Right_1": {"x_0": 165723 + 0, "y_0": 81900 - 100, "x_1": 168163 + 100, "y_1": 89300 + 100}, #x 9
                            "Finger_1": {"x_0": 85640 - 140, "y_0": 34850 - 100, "x_1": 95890 + 110, "y_1": 83400 - 0}, #x 4
                            "Finger_2": {"x_0": 106600 - 100, "y_0": 34850 - 100, "x_1": 118580 + 110, "y_1": 83400 - 0}, #x 5
                            "Finger_3": {"x_0": 130890 - 100, "y_0": 34850 - 100, "x_1": 141340 + 110, "y_1": 83400 - 0}, #x 7
                            "Finger_4": {"x_0": 150615 - 100, "y_0": 34850 - 100, "x_1": 165723 - 1, "y_1": 83400 - 0}, #x 8
                            }
CHARGING_STATION_COORDINATION = {"Charging_Station_Left_1": {"x_0": 84220 - 300, "y_0":  80410 - 100, "x_1": 84220 + 300, "y_1": 86500 + 100},
                                "Charging_Station_Left_2": {"x_0": 89640 - 300, "y_0": 86500 - 100, "x_1": 89640 + 300, "y_1": 93800 + 100},
                                 "Battery_Swap_Station_Left": {"x_0": 115800 - 300, "y_0": 91000 - 100, "x_1": 118245 - 141, "y_1": 99193 + 100},
                                 "Battery_Swap_Station_Right": {"x_0": 132205 - 300, "y_0": 91000 - 100, "x_1": 134800 - 141, "y_1": 100000 + 100}
                                 }

# RCS Parameters
MainTaskStatusDict  = {"Time Out": "11",
                         "Created": "1",
                         "executing": "2",
                         "cancelled": "5",
                         "Picking": "7",
                         "Completed": "9"
                         }

SubTaskStatuDict = {"Time Out": 11,
                         "Created": 1,
                         "executing": 2,
                         "cancelled": 5,
                         "Picking": 7,
                         "Completed": 9
                         }


# DataBase Constant
MONGODB_LOCAL_URL = "mongodb://localhost:27017/"
MONGODBNAME_AGVSTATISTICS = "AGV_Statistics"

MONGODBNAME_AGVSTATISTICS_VOLUME= "AGV_Statistics_Volume"
MONGODBNAME_AGVSTATISTICS_VOLUME_PickedVolumeTaskStatistics = "PickedVolumeTaskStatistics"
MONGODBNAME_AGVSTATISTICS_VOLUME_MinutelyPickedVolumeTaskStatistics = "MinutelyPickedVolumeTaskStatistics"
MONGODBNAME_AGVSTATISTICS_VOLUME_UnCompletedTaskStatistics = "UnCompletedTaskStatistics"
MONGODBNAME_AGVSTATISTICS_VOLUME_CompletedTaskStatistics = "CompletedTaskStatistics"

MONGODBNAME_AGVERRORSENDING = "AGV_ErrorSending"
MONGODBNAME_USERIDLISTCOLLECTION = "AGV_UserIdListCollection"

MONGODBNAME_TELEGRAMSTAT = "TG_Statistics"

MONGODBNAME_FUNCTIONTIMER = "FunctionTimerDB"

MONGODBNAME_ALARMFUNCTIONTIMER = "ALARMFunctionTimerDB"

# Orcale DataBase Configuration
ORCALE_URL = "HKW1LAGVDB-VIP.aswatson.net"
ORCALE_PORT = "1523"
ORACLE_SERVICENAME = "PSHKPAGV"


# algorithm syntax dictionary
AlgorithmSyntaxDict = {"$lt": "<", "$lte": "<=", "$gt": ">", "$gte": ">=", "$eq": "=", "neq": "!="}
LogicSyntaxDict = {"$and": "and", "$or": "or"}

# Telegram CONSTANT
MAX_MESSAGE_LENGTH = 4000

#Color Map
CMAP = {
'aliceblue':            '#F0F8FF',
'antiquewhite':         '#FAEBD7',
'aqua':                 '#00FFFF',
'aquamarine':           '#7FFFD4',
'azure':                '#F0FFFF',
'beige':                '#F5F5DC',
'bisque':               '#FFE4C4',
'black':                '#000000',
'blanchedalmond':       '#FFEBCD',
'blue':                 '#0000FF',
'blueviolet':           '#8A2BE2',
'brown':                '#A52A2A',
'burlywood':            '#DEB887',
'cadetblue':            '#5F9EA0',
'chartreuse':           '#7FFF00',
'chocolate':            '#D2691E',
'coral':                '#FF7F50',
'cornflowerblue':       '#6495ED',
'cornsilk':             '#FFF8DC',
'crimson':              '#DC143C',
'cyan':                 '#00FFFF',
'darkblue':             '#00008B',
'darkcyan':             '#008B8B',
'darkgoldenrod':        '#B8860B',
'darkgray':             '#A9A9A9',
'darkgreen':            '#006400',
'darkkhaki':            '#BDB76B',
'darkmagenta':          '#8B008B',
'darkolivegreen':       '#556B2F',
'darkorange':           '#FF8C00',
'darkorchid':           '#9932CC',
'darkred':              '#8B0000',
'darksalmon':           '#E9967A',
'darkseagreen':         '#8FBC8F',
'darkslateblue':        '#483D8B',
'darkslategray':        '#2F4F4F',
'darkturquoise':        '#00CED1',
'darkviolet':           '#9400D3',
'deeppink':             '#FF1493',
'deepskyblue':          '#00BFFF',
'dimgray':              '#696969',
'dodgerblue':           '#1E90FF',
'firebrick':            '#B22222',
'floralwhite':          '#FFFAF0',
'forestgreen':          '#228B22',
'fuchsia':              '#FF00FF',
'gainsboro':            '#DCDCDC',
'ghostwhite':           '#F8F8FF',
'gold':                 '#FFD700',
'goldenrod':            '#DAA520',
'gray':                 '#808080',
'green':                '#008000',
'greenyellow':          '#ADFF2F',
'honeydew':             '#F0FFF0',
'hotpink':              '#FF69B4',
'indianred':            '#CD5C5C',
'indigo':               '#4B0082',
'ivory':                '#FFFFF0',
'khaki':                '#F0E68C',
'lavender':             '#E6E6FA',
'lavenderblush':        '#FFF0F5',
'lawngreen':            '#7CFC00',
'lemonchiffon':         '#FFFACD',
'lightblue':            '#ADD8E6',
'lightcoral':           '#F08080',
'lightcyan':            '#E0FFFF',
'lightgoldenrodyellow': '#FAFAD2',
'lightgreen':           '#90EE90',
'lightgray':            '#D3D3D3',
'lightpink':            '#FFB6C1',
'lightsalmon':          '#FFA07A',
'lightseagreen':        '#20B2AA',
'lightskyblue':         '#87CEFA',
'lightslategray':       '#778899',
'lightsteelblue':       '#B0C4DE',
'lightyellow':          '#FFFFE0',
'lime':                 '#00FF00',
'limegreen':            '#32CD32',
'linen':                '#FAF0E6',
'magenta':              '#FF00FF',
'maroon':               '#800000',
'mediumaquamarine':     '#66CDAA',
'mediumblue':           '#0000CD',
'mediumorchid':         '#BA55D3',
'mediumpurple':         '#9370DB',
'mediumseagreen':       '#3CB371',
'mediumslateblue':      '#7B68EE',
'mediumspringgreen':    '#00FA9A',
'mediumturquoise':      '#48D1CC',
'mediumvioletred':      '#C71585',
'midnightblue':         '#191970',
'mintcream':            '#F5FFFA',
'mistyrose':            '#FFE4E1',
'moccasin':             '#FFE4B5',
'navajowhite':          '#FFDEAD',
'navy':                 '#000080',
'oldlace':              '#FDF5E6',
'olive':                '#808000',
'olivedrab':            '#6B8E23',
'orange':               '#FFA500',
'orangered':            '#FF4500',
'orchid':               '#DA70D6',
'palegoldenrod':        '#EEE8AA',
'palegreen':            '#98FB98',
'paleturquoise':        '#AFEEEE',
'palevioletred':        '#DB7093',
'papayawhip':           '#FFEFD5',
'peachpuff':            '#FFDAB9',
'peru':                 '#CD853F',
'pink':                 '#FFC0CB',
'plum':                 '#DDA0DD',
'powderblue':           '#B0E0E6',
'purple':               '#800080',
'red':                  '#FF0000',
'rosybrown':            '#BC8F8F',
'royalblue':            '#4169E1',
'saddlebrown':          '#8B4513',
'salmon':               '#FA8072',
'sandybrown':           '#FAA460',
'seagreen':             '#2E8B57',
'seashell':             '#FFF5EE',
'sienna':               '#A0522D',
'silver':               '#C0C0C0',
'skyblue':              '#87CEEB',
'slateblue':            '#6A5ACD',
'slategray':            '#708090',
'snow':                 '#FFFAFA',
'springgreen':          '#00FF7F',
'steelblue':            '#4682B4',
'tan':                  '#D2B48C',
'teal':                 '#008080',
'thistle':              '#D8BFD8',
'tomato':               '#FF6347',
'turquoise':            '#40E0D0',
'violet':               '#EE82EE',
'wheat':                '#F5DEB3',
'white':                '#FFFFFF',
'whitesmoke':           '#F5F5F5',
'yellow':               '#FFFF00',
'yellowgreen':          '#9ACD32'}



# CronJob Constant Properties

# DataBase Properties
CRON_DATABASE_NAME = "CRON_DATABASE_NAME"