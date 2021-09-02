# from utils.sensor_builder import OutBoundManager
# from utils.Web_Rcs import Web_RCS

class TaskDict(dict):
    # SubTaskStatuDict = Web_RCS.SubTaskOrderService.SubTaskStatuDict

    def __init__(self):
        dict.__init__(self)
        # init key in the dictionary
        for key in TaskDict.SubTaskStatuDict.keys():
            self[key] = None

    def extend(self, newDict):
        if type(newDict).__name__ != "dict" or type(newDict).__name__ != "TaskDict":
            raise Exception("Only dict type can be extended into taskDict")

        for key, value in newDict.items():
            if key not in self.keys():
                self[key] = value

        return self

    def addDict(self, dict):
        for key, value in dict.items():
            self[key]


    def update(self, newDict):
        statusChangedTaskIDList = []
        if type(newDict).__name__ != "dict" or type(newDict).__name__ != "TaskDict":
            raise Exception("Only dict type can be extended into taskDict")
        for key, value in newDict.items():
            if key in self.keys():
                self[key] = value
                statusChangedTaskIDList.extend(key)
            else:
                raise Exception("Some taskId is missing: {}".format(key) )

        return statusChangedTaskIDList

# class TaskInfo():
#
#     def __init__(self, targetX, targetY):
#         self.targetX = ""
#         self.targetY = ""
#         self.outboundLocation = ""
#
#     def updatedCoordination(self, cooX, cooY):
#         self.targetX = cooX
#         self.targetY = cooY
#         self._updateoutBoundLocation()
#         return self
#
#     def _updateoutBoundLocation(self):
#         self._setOutBoundLocation(OutBoundManager.getLocationByCoordination(self.targetX, self.targetY))
#         return self
#
#     def _setOutBoundLocation(self, outBoundLocation):
#         self.outboundLocation = outBoundLocation
#         return self

