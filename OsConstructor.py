import os, subprocess, psutil

class OsConstructor:

    def __init__(self):
        pass

    def getLogInfo(self, deep):
        file = os.path.join(os.path.dirname(__file__), '..', 'YobitTrader', 'YobitTrader.log')
        content = open(file, "r")
        lines = content.readlines()
        content.close()
        i = lines.__len__() - deep
        text = ""

        while i < lines.__len__():
            text += lines[i]
            i += 1

        return text

    def checkYobitTraiderProcess(self, pid):
        code = True
        if psutil.pid_exists(pid) == False:
            code = False
        return code

    def restartYobitService(self, pid):
        code = 0
        if psutil.pid_exists(pid) == False:
            return_value = subprocess.run(["python3 main.py &"], cwd="/home/YobitTrader", capture_output=True,
                                      text=True)
            code = return_value.returncode
        return code