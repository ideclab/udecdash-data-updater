import os, logging, re
from subprocess import Popen, PIPE

class Queue():

    def startAll(self):
        logging.debug("STOPING SUPERVISOR")
        command = self.__buildCommand("start all")
        sudo_password = os.getenv('SERVER_SUDO_PASSWORD')
        p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
        result = p.communicate(sudo_password + '\n')[1]
        return self.__checkStatus(result, "started")

    def stopAll(self):
        logging.debug("STOPING SUPERVISOR")
        command = self.__buildCommand("stop all")
        sudo_password = os.getenv('SERVER_SUDO_PASSWORD')
        p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
        result = p.communicate(sudo_password + '\n')[1]
        return self.__checkStatus(result, "stopped")

    def refresh(self):
        logging.debug("REFRESH SUPERVISOR")
        command = self.__buildCommand("reread")
        sudo_password = os.getenv('SERVER_SUDO_PASSWORD')
        p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
        p.communicate(sudo_password + '\n')[1]
        command = self.__buildCommand("update all")
        p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
        p.communicate(sudo_password + '\n')[1]
      


    def __checkStatus(self, result, status):
        lines = result.split("\n")
        lines =list(filter(str.strip, lines))
        for line in lines:
            expression = ".+"+status+"$"
            print(expression)
            exp = re.compile(expression)
            if not exp.match(line):
                return False
        return True

    def __buildCommand(self, command):
        supervisord_path = os.getenv('SERVER_SUPERVISORD_COMMAND_PATH')
        output = '{} {}'.format(supervisord_path, command).split()
        return output