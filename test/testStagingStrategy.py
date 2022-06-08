from utils.Web_Rcs_14_04_22 import Web_RCS
import json

if __name__ == "__main__":
    loginService = Web_RCS.LoginService()
    loginService.runService()

    view = Web_RCS.StagingStrategySettingServiceView()
    add = Web_RCS.StagingStrategySettingServiceAdd()
    delete = Web_RCS.StagingStrategySettingServiceDelete()
    deploy = Web_RCS.StagingStrategySettingServiceDeploy()


    viewList = json.loads(view.sendJSON().text)["data"]



    # add.setId("3").setStart("16:00").setEnd("16:30").setFreeTime("16:30").setFreeInterval("50")
    # response = json.loads(add.sendJSON().text)

    delete.setId("3")
    response = json.loads(delete.sendJSON().text)

    deploy.sendJSON()
    response = json.loads(deploy.sendJSON().text)
    print("")