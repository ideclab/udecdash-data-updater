import os
import logging
from datetime import datetime
from Dashboard.Helpers.BaseDirectory import BaseDirectory
class LoadEvent:
    def success(self, table_name, file_path):
        self.__saveSuccessEvent(table_name, file_path)
        logging.debug("DEFAULT SUCCESS EVENT WAS CALLED")
    
    def failed(self, table_name, file_path, error):
        logging.debug("DEFAULT FAILED EVENT WAS CALLED")

    def account_dim_success(self, table_name, file_path):
        self.__saveSuccessEvent(table_name, file_path)
        logging.debug("LOAD EVENT account_dim_success SUCCESSFULLY")

    def requests_success(self, table_name, file_path):
        directory = BaseDirectory()
        file_name = directory.purgeBasePath(file_path, table_name)
        exists_in_db =self._getRequestRegistered(file_name)
        if(exists_in_db):
            self.__updateSuccessEvent(file_name)
        self.__saveSuccessEvent(table_name, file_path)
        logging.debug("LOAD EVENT requests_success SUCCESSFULLY")

    def account_dim_failed(self, table_name, file_path, error):
        logging.debug("LOAD EVENT account_dim_failed FAILED")

    def __updateSuccessEvent(self, file_name):
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        query="""UPDATE package_files_loaded SET status = %s,updated_at = %s WHERE file_name = %s"""
        values = ['outdated', now, file_name]
        self.insert(query, values)


    def __saveSuccessEvent(self, table_name, file_path):
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        directory = BaseDirectory()
        instance_id = int(os.getenv('INSTANCE_ID'))
        file_name = directory.purgeBasePath(file_path, table_name)
        file_size = directory.getFileSize(file_path)
        query="""INSERT INTO package_files_loaded(instance, table_name, file_name, status,file_size, created_at) 
        VALUES (%s, %s, %s, %s,%s, %s)"""
        values = [instance_id, table_name, file_name, "success",file_size, now]
        self.insert(query, values)
    
    # def saveFailedEvent(self, table_name, file_name, status, error_detail = None):
    #     query="INSERT INTO package_files_loaded (created_at) VALUES (%s)"
    #     now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    #     values = [str(now)]
    #     logging.debug("UPDATE INSTANCE ID => {}".format(instance_id))
    #     return instance_id

        # id SERIAL PRIMARY KEY,
        #     instance INTEGER NOT NULL,
        #     table_name VARCHAR(256) NOT NULL,
        #     file_name VARCHAR(256) NOT NULL,
        #     status VARCHAR(100) NOT NULL,
        #     error_details TEXT

