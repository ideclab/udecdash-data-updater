import os
import subprocess
import logging
import re
import time
from Dashboard.Helpers.Notification import Notification


class Download:
    def __init__(self):
        self._PATH_CANVAS_CONFIG = os.getenv('PATH_CANVAS_CONFIG')
        self._downloadStatus = False

    def start(self):
        beartruth = True
        total_errors= 0
        while beartruth == True:
            try:
                command = "{} sync -c config.js".format(os.getenv('SERVER_CANVAS_DATA_CLI_COMMAND_PATH'))
                file_download = subprocess.run(
                    command, cwd=self._PATH_CANVAS_CONFIG, shell=True, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as err:
                logging.debug('error')
                self.__cleanMessage(err)
                self._downloadStatus = False
                beartruth = False
            else:
                if(file_download.returncode != 0):
                    if(total_errors == 3):
                        self.__cleanMessage(file_download.stderr.decode('utf-8'))
                        self._downloadStatus = False
                        beartruth = False
                    else:
                        total_errors+=1
                        time.sleep(60)
                else:
                    beartruth = False
                    self._downloadStatus = True
                
    def downloadClaim(self):
        return self._downloadStatus

    def __cleanMessage(self, message):
        notification=Notification()
        notification.setMessage(message)
        notification.submit()
