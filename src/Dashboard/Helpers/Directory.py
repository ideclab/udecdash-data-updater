from Dashboard.DatabaseManager.DB import DB
import pandas as pandas
from Dashboard.Helpers.BaseDirectory import BaseDirectory
import logging


class Directory(BaseDirectory):

    def __init__(self):
        super().__init__()
        self._db = DB()

    def getFilesPath(self, table_name):
        paths = []
        base_path = self._getBasePath(table_name)
        if table_name == 'requests':
            files = self._getRequestFilesNameNotLoaded()
        else:
            files = self._getFilesName(table_name)
        for name in files:
            full_path = "{}{}{}".format(base_path, self._PATH_CONCAT, name)
            paths.append(full_path)
        return paths

    def _getLoadedRequestFiles(self):
        query = "select distinct(file_name),file_size from package_files_loaded where table_name = 'requests' and status != 'outdated'"
        rows = self._db.select(query)
        if(self._FIRST_DATA_UPDATE):
            existing = []
            for row in rows:
                existing.append(row[0])
        else:
            column_names = ["request", "size"]
            existing = pandas.DataFrame(rows, columns=column_names)

        return existing
