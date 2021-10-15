import io
from os import getenv, path, environ
import csv
import logging
import pandas as pandas
from Dashboard.Constants import CUSTOM_TABLE_HEADERS, USECOLS
from Dashboard.DatabaseManager.DB import DB
from Dashboard.Helpers.Directory import Directory
from Dashboard.LoaderManager.DataFilter import DataFilter

class DataLoader: 
    
    def __init__(self):
        self.__db = DB()
        self.__directory = Directory()
        self.__data_filter = DataFilter()
        self._FIRST_DATA_UPDATE= getenv('FIRST_DATA_UPDATE', 'False') == 'True'


    def start(self):    
        tables = self.__db.getCleanableTables()
        for table_name in tables:
            self.__loadData(table_name)
        self.__loadData("requests")

    def __loadData(self, table_name):
        files_path = self.__directory.getFilesPath(table_name)
        if "FILE_EXTENSION" in environ:
            for file_path in files_path:
                root,extension = path.splitext(file_path)
                if(extension == "."+getenv('FILE_EXTENSION')):
                    self.__loadFinalData(table_name,file_path)
        else:
            for file_path in files_path: 
                self.__loadFinalData(table_name,file_path)

                
    def __loadFinalData(self,table_name,file_path):
        headers = CUSTOM_TABLE_HEADERS.get(table_name, None)
        dataframe = self.__getDataframe(file_path, table_name)
        ioContent = self.__dataframeToIoContent(dataframe)                     
        self.__db.migrateDataToTable(ioContent, table_name, headers, file_path=file_path)

    def __getDataframe(self, file_path, table_name):
        cols = USECOLS.get(table_name, None)
        if cols == None: 
            dataframe = pandas.read_csv(file_path, compression='gzip', header = None, 
                sep='\t', quoting=csv.QUOTE_NONE, error_bad_lines=False,
                low_memory=False, encoding='utf-8')
        else:
            dataframe = pandas.read_csv(file_path, compression='gzip', header = None, 
                sep='\t', quoting=csv.QUOTE_NONE, error_bad_lines=False, usecols= cols,
                low_memory=False, encoding='utf-8')
        dataframe = self.__applyFilters(dataframe, table_name)
        if(not(self._FIRST_DATA_UPDATE) and (table_name == 'requests')):
            request_name = self.__directory.purgeBasePath(file_path,table_name)
            dataframe = self.__db.bringMissingData(dataframe,request_name)
        return dataframe

    def __applyFilters(self, dataframe, table_name):
        try:
            filterFunction = getattr(self.__data_filter, "{}_filter".format(table_name))
            dataframe = filterFunction(dataframe)
        except AttributeError:
            pass
        return dataframe
    
    def __dataframeToIoContent(self, dataframe):
        output = io.StringIO()
        dataframe.to_csv(output, sep='\t', header=False, index=False, encoding='utf-8')
        output.seek(0)
        return output
