import logging
import glob
from os import path, listdir, getenv,environ
from Dashboard.Constants import CANVAS_TABLES
import shutil
import pandas as pandas


class BaseDirectory():

    def __init__(self):
        # logging.basicConfig(level=int(os.getenv('DEBUG_LEVEL')))
        self._PATH_DATA_FILES = getenv('PATH_DATA_FILES')
        self._PATH_CONCAT = getenv('PATH_CONCAT')
        self._FIRST_DATA_UPDATE = getenv(
            'FIRST_DATA_UPDATE', 'False') == 'True'
      

    def purgeBasePath(self, file_path, table_name):
        base_path = self._getBasePath(table_name)
        to_clear = "{}{}".format(base_path, self._PATH_CONCAT)
        return self._removePrefix(file_path, to_clear)

    def getFileSize(self, file_path):
        return path.getsize(file_path)

    def _removePrefix(self, text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    def tablesHasFoldersWithFiles(self):
        valid = True
        for table_name in CANVAS_TABLES:
            directory = self._getBasePath(table_name)
            if not self._hasFiles(directory):
                valid = False
                logging.error(
                    "Table {} not has files or directory not exists".format(table_name))
        logging.debug("All tables has his folders with files: " + str(valid))
        return valid

    def _getFilesName(self, table_name):
        path = self._getBasePath(table_name)
        return listdir(path)

    def _getRequestFilesNameNotLoaded(self):
        available = self._getAllRequestFiles()
        loaded = self._getLoadedRequestFiles()
        if(self._FIRST_DATA_UPDATE):
            not_loaded = list(set(available) - set(loaded))
        else:
            not_loaded = self._getAllMissingData(available, loaded)
        logging.debug("REQUESTS => Loaded {}, Available: {}, For load: {}".format(
            len(loaded), len(available), len(not_loaded)))
        return not_loaded

    def _getAllMissingData(self, available, loaded):
        valid_request = loaded.request.isin(available.request)
        loaded = loaded[(valid_request)]
        all_requests = pandas.concat(
            [available, loaded]).reset_index(drop=True)
        remove_duplicates = all_requests.drop_duplicates(keep=False)
        filter_duplicates = remove_duplicates.drop_duplicates(subset=[
                                                              'request'])
        return filter_duplicates['request'].to_numpy()

    def _getAllRequestFiles(self):
        path = self._getBasePath("requests")
        files_list = listdir(path)
        if(self._FIRST_DATA_UPDATE):
            return files_list
        else:
            files = pandas.DataFrame(columns=['request', 'size'])
            for i in range(len(files_list)):
                file_path = "{}{}{}".format(
                    path, self._PATH_CONCAT, files_list[i])
                files = files.append({'request': files_list[i], 'size': self.getFileSize(
                    file_path)}, ignore_index=True)
            return files

    def _getBasePath(self, table_name):
        return "{}{}{}".format(self._PATH_DATA_FILES, self._PATH_CONCAT, table_name)

    def _hasFiles(self, directory):
        has_files = False
        if path.isdir(directory) and len(listdir(directory)) > 0:
            if "FILE_EXTENSION" in environ:
                if len(glob.glob1(directory,"*."+getenv('FILE_EXTENSION'))) > 0:
                    has_files = True
            else:
                has_files = True
        return has_files

    def deleteFileDirectories(self):
        for table_name in CANVAS_TABLES:
            if(table_name != 'requests'):
                directory = self._getBasePath(table_name)
                if path.isdir(directory):
                    shutil.rmtree(directory)
                    print('eliminado {}', directory)
