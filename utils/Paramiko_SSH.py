import paramiko
import os
import io
import datetime
import os
import subprocess
import time

class SSH_Connection:
    def __init__(self):
        # Variable(s)
        self.connected = False
        # Init
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    def connect(self, ip, port, username, password):
        try:
            self.client.connect(hostname=ip, port=port, username=username, password=password)
            self.connected = True
            print("Connect Successfully")
        except :
            self.connected = False
            print("Connection False")
            raise Exception("Connection False")
        return self

    def exec(self, command, timeout=None):
        if not self.connected:
            raise Exception("Please connect host before execute command")
        stdin, stdout, stder = self.client.exec_command(command, get_pty=True, timeout=timeout)
        output = ""
        try:
            output = stdout.read().decode("utf-8")
        except Exception as e:
            print("Error")
        return output
        # if stder:
        #     return stder


class LowerBatteryService():
    def __init__(self):
        self.params = {}
        self._initParam()

    def _initParam(self):
        self.params["param.clientCode"] = ""
        self.params["ipAddress"] = ""
        self.cmd = ""

    def setAGVIP(self, ipAddress):
        self.params["ipAddress"] = ipAddress
        return self

    def setLowerBattery(self):
        self.cmd = 'castor_cli -R "95 1242 0 3 30"'
        return self

    def resumeNormalBattery(self):
        self.cmd = 'castor_cli -R "95 6610 0 3 30"'
        return self

    def sendJSON(self):
        ssh = SSH_Connection()
        ssh.connect(self.params["ipAddress"], 22, "root", "hiklinux")
        output = ssh.exec(self.cmd)
        return output


class ShutDownAGVService():
    def __init__(self):
        self.params = {}
        self._initParam()

    def _initParam(self):
        self.params["param.clientCode"] = ""
        self.params["ipAddress"] = ""
        self.cmd = ""

    def setAGVIP(self, ipAddress):
        self.params["ipAddress"] = ipAddress
        return self

    def shutdownAGV(self):
        self.cmd = "/sbin/halt"
        # self.cmd = "/sbin/date"
        return self

    def sendJSON(self):
        ssh = SSH_Connection()
        ssh.connect(self.params["ipAddress"], 22, "root", "hiklinux")
        output = ssh.exec(self.cmd, timeout=10)
        return output

def putty_cmd(ip, account, pw, cmd_file):
    putty_str = "D:\\Software\\putty\\putty.exe -ssh {}@{} -pw {} -m {} -t".format(account, ip, pw, cmd_file)
    result = subprocess.Popen(putty_str)
    time.sleep(15)
    return ip

def getTimeRangeFileList(targetList):
    resultList = []
    for targetFile in targetList:
        hour = int(targetFile.split("_")[4])
        if hour >= 14 and hour <= 20:
            resultList.append(targetFile)
    return resultList


class logger:

    def __init__(self):
        print("Current Working Directory is: " + os.getcwd())
        self.targetFile = ""
        self.closed = True
        self.cursor = None

    def setTarget(self, target):
        self.targetFile = target
        return self

    def getCursor(self):
        self.closed = False
        if self.cursor:
           self.cursor.close()
        if self.targetFile:
            self.cursor = open(self.targetFile, "a+", encoding="utf-8")
            return self.cursor
        raise Exception("Target is not available")

    def write(self, data):
        if self.closed == True:
            self.getCursor()
            self.closed = False
        self.getCursor().write(data + "\n")
        print("Data is written successfully: " + str(data))
        self.getCursor().close()
        return self



IP = "10.39.10.{}"
START_IP = 8
END_IP = 9

if __name__ == "__main__":
    SSH = SSH_Connection()

    logger2 = logger()
    with open("linux_cmd_getBMS.txt", "r+") as file:
        cmd = file.read()
    print(cmd)
    # targetIPRange = [IP.format(i) for i in range(START_IP, END_IP + 1)]
    targetIPRange = open("targetAGVIPTable.txt", "r+").read().split("\n")
    for ip in targetIPRange:
        # try:
        #     SSH.connect(ip=ip, port=22, username="root", password="hiklinux")
        #     now = "[{} ]".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #     msg = ip + ": Connection Success"
        #     logger2.write(now + msg)
        # except Exception:
        #     print("Connection Error")
        #     now = "[{} ]".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #     msg = ip + ": Connection Failed"
        #     logger2.write(now + msg)
        #     continue

        # output = SSH.exec(cmd)
        cmd_fileName = "D:\\Software\\putty\\linux_cmd_getBMS.txt"
        output2 = putty_cmd(ip, "root", "hiklinux", cmd_fileName)
        # print(output)
        print("\n\n")
        print(output2)
        # targetLogFiles = [b for b in output.split("\n") if b != ""]

        # targetLogFiles = getTimeRangeFileList(targetLogFiles)
        # print(targetLogFiles)

        # for logfile in targetLogFiles:
        #     cmd_str = "cd /mnt; sz {}".format(logfile)
        #     tmpfileName = logfile + ".txt"
        #     file = open(tmpfileName, "w+")
        #     file.write(cmd_str)
        #     file.close()
        #     print(cmd_str)
        #     output = putty_cmd(ip, "root", "hiklinux", tmpfileName)
        #     # time.sleep(15)
        #     # os.remove(tmpfileName)

        now = "[{}]".format( datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # logger.getCursor().write(now + output)
        START_IP += 1

    print("")



