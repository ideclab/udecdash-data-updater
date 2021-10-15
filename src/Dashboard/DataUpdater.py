import os
import logging
from datetime import datetime
from Dashboard.DatabaseManager.DB import DB
from Dashboard.Helpers.Directory import Directory
from Dashboard.Helpers.Notification import Notification
from Dashboard.DownloadManager.Download import Download
from Dashboard.QueueManager.Queue import Queue
from Dashboard.LoaderManager.DataLoader import DataLoader
from Dashboard.Helpers.SiteStatus import SiteStatus


class DataUpdater():
    def __init__(self):
        self.__db = DB()
        self.__db.createPackageTables()
        self.__queue = Queue()
        self.__directory = Directory()
        self.__dataloader = DataLoader()
        self.__sitestatus = SiteStatus()
        

    def launch(self):
        try:
            self.__deleteFolders()
            if(self.__downloadData()):
                if self.__fullDirectories():
                    self.__updateData()
                else:
                    notification = Notification()
                    notification.setMail()
                    notification.setMessage(
                        "Canvas data not has a valid download, the data was not processed")
                    notification.submit()
            else:
                notification = Notification()
                notification.setMail("Descarga Falló")
        except NameError:
            notification = Notification()
            notification.setMail(NameError)
            raise Exception(NameError)

    def __downloadData(self):
        if os.getenv('ENABLE_DOWNLOAD') != 'True':
            return True
        download = Download()
        download.start()
        return download.downloadClaim()

    def __deleteFolders(self):
        if os.getenv('CLEAR_DIRECTORIES_BEFORE_DOWNLOAD') == 'True':
            self.__directory.deleteFileDirectories()
        pass

    def __fullDirectories(self):
        return self.__directory.tablesHasFoldersWithFiles()

    def __updateData(self):
        os.environ['INSTANCE_ID'] = str(self.__createUpdateInstance())
        self.__sitestatus.updatingData()
        self.__queue.stopAll()
        self.__db.truncateTables()
        self.__dataloader.start()
        self.__queue.startAll()
        self.__sitestatus.enable()

    def __createUpdateInstance(self):
        query = "INSERT INTO package_updates_instance (created_at) VALUES (%s)"
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        values = [str(now)]
        instance_id = self.__db.insertReturningId(query, values)
        logging.debug("UPDATE INSTANCE ID => {}".format(instance_id))
        return instance_id
