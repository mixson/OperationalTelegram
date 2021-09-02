import os, sys
currentDir = "\\".join(os.getcwd().split("\\")[0:-1])
sys.path.insert(0, currentDir)
import re

from values import CONSTANT


if __name__ == "__main__":

    morningStartTime = ""
    morningEndTime = ""

    nightStartTime = ""
    nightEndTime = ""

    morningStartTime = input("Morning Start Time:")
    morningEndTime = input("Morning End Time:")

    nightStartTime = input("Night Start Time:")
    nightEndTime = input("Night End Time:")

    with open(os.path.join(CONSTANT.MRTA_CONFIG_LOCATION), encoding="utf-8") as file:
        text = file.read()
        texts = str(text)
        targetList = ["<MRTA_SET_T>(.*)</MRTA_SET_T>",
                      "<MRTA_SET_PICK_T>(.*)</MRTA_SET_PICK_T>",
                      "<MRTA_SET_T_PM>(.*)</MRTA_SET_T_PM>",
                      "<MRTA_SET_PICK_T_PM>(.*)</MRTA_SET_PICK_T_PM> "]

        replaceList = ["<MRTA_SET_T>{}</MRTA_SET_T>".format(morningStartTime),
                      "<MRTA_SET_PICK_T>{}</MRTA_SET_PICK_T>".format(morningEndTime),
                      "<MRTA_SET_T_PM>{}</MRTA_SET_T_PM>".format(nightStartTime),
                      "<MRTA_SET_PICK_T_PM>{}</MRTA_SET_PICK_T_PM> ".format(nightEndTime)]

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


    print()
    with open(os.path.join(currentDir, "values", "rcs_mrta_config.xml"), "w" , encoding="utf-8") as file:
        file.write(text)
