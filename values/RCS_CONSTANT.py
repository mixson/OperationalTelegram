MAX_MESSAGE_LENGTH = 4000


MRTA_CONFIG_LOCATION = r"D:\program\OperationalTelegram\values\rcs_mrta_config.xml"
# MRTA_CONFIG_LOCATION = r"D:\hikvision\HikServer\rcs\rcs_mrta_config.xml"

STAGINGPICKE_FILENAME = "dailyStaging.pkl"
QUEUEPICKE_FILENAME = "dailyStaging.pkl"

# ROUTE_FILENAME_DICT = {"dailyStaging": "dailyStaging.pkl", "RF_dailyStagingV2": "RF_dailyStagingV2.pkl",
#                        "queueNumberKeep": "queueNumberKeep.pkl", "queueSetEdit": "queueSetEdit.pkl", "stagingNumMonitor": "stagingNumMonitor.pkl"}
ROUTE_FILENAME_DICT = {"dailyStaging": "dailyStaging.pkl"
                       } # debug
# ROUTE_FILENAME_DICT = { "queueSetEdit": "queueSetEdit.pkl"}
SUBSCIRPTION_DICT = {"queueChangeNotification": "queueChangeNotification.pkl", "stagingChangeNotification": "stagingChangeNotification.pkl", "stationChangeNotification": "stationChangeNotification.pkl"}

QUEUE_RULE_DICT = {"North": "^MOUT", "East": "^RMIN", "South": "^$", "West1": "^LMIN(0[4-6])$", "West2": "^LMIN(0[7-9]|1[0-9])$"}
QUEUE_INCREASE_NUMBER_DICT = {"North": 1, "East": 30, "South": 1, "West1": 30, "West2": 30}
QUEUE_RESUME_NUMBER_DICT = {"North": 3, "East": 2, "South": 1, "West1": 4, "West2": 3}