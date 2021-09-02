from utils.Web_Rcs import Web_RCS

import JSON

if __name__ == "__main__":
    taskIdList = []
    subTaskService = Web_RCS.SubTaskOrderService()

    taskDict = {}
    for taskId in taskIdList:
        subTaskService.selectTaskID(taskId)
        dataList = subTaskService.sendJSON()