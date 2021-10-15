import os
import logging
import psycopg2
from Dashboard.Constants import * 
from Dashboard.DatabaseManager.PackageTables import PACKAGE_TABLES
from Dashboard.DatabaseManager.LoadEvent import LoadEvent
import pandas as pandas

class DB(LoadEvent):
    def __init__(self):
        self.__load_event = LoadEvent()
        logging.debug('DB Instance => Host: {} Port: {} db_name: {} User: {} Password: {}'.format(
            os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME'),
            os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD')))

    def getConnection(self):
        connection = None
        try:
            connection = psycopg2.connect(database = os.getenv('DB_NAME'), 
            user = os.getenv('DB_USERNAME'), password = os.getenv('DB_PASSWORD'), 
            host = os.getenv('DB_HOST'), port = os.getenv('DB_PORT'))
            connection.autocommit = False
            connection.set_client_encoding('utf-8')
        except:
            print("Database connection failed")
        return connection
    
    def insertReturningId(self, query, values = []):
        row_id = None
        query = "{} RETURNING id;".format(query)
        logging.debug("SQL QUERY => {} params: {}".format(query, values))
        try:
            connection = self.getConnection()
            cursor = connection.cursor()
            cursor.execute(query, values)
            row_id = cursor.fetchone()[0]
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            logging.error("SQL Query failed => {}".format(str(error)))
        finally:
            cursor.close()
            connection.close()
        return row_id
    
    def insert(self, query, values = []):
        valid = False
        row_id = self.insertReturningId(query, values)
        if row_id > 0:
            valid = True
        return valid

    def bringMissingData(self,dataframe,request_name):
        incomplete_file =self._getRequestRegistered(request_name)
        logging.debug("total de datos antes {}".format(len(dataframe.index)))
        if(incomplete_file):
            logging.debug("si")
            query = "SELECT id FROM requests"
            request = self.select(query)
            request_id = pandas.DataFrame(request, columns = ['id'])
            valid_request =~dataframe[0].isin(request_id.id)
            dataframe = dataframe[(valid_request)]
        logging.debug("total de datos despues {}".format(len(dataframe.index)))
        return dataframe


    def createPackageTables(self):
        for table_definition in PACKAGE_TABLES:
            self.executeQuery(table_definition)
    
    def select(self, query):
        rows = []
        try:
            connection = self.getConnection()
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            logging.error("SQL Query failed => {}".format(str(error)))
        finally:
            cursor.close()
            connection.close()
        return rows

    def executeQuery(self, query):
        connection = self.getConnection()
        cursor = connection.cursor()
        logging.debug("SQL QUERY => {}".format(query))
        try:
            cursor.execute(query)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("SQL Query failed => {}".format(str(error)))
        finally:
            cursor.close()
            connection.close()
    
    def truncateTables(self):
        for table_name in self.getCleanableTables():
            sql = "truncate table {}".format(table_name)    
            self.executeQuery(sql)
    
    def getCleanableTables(self):
        tables = []
        for table_name in CANVAS_TABLES:
            if not table_name in TRUNCATE_TABLES_EXCEPTION:
                tables.append(table_name)
        return tables
    def migrateDataToTable(self, ioContent, table_name, headers = None, file_path = None):
        connection = self.getConnection()
        cursor = connection.cursor()
        try:
            logging.debug("Migrating file for table: {}".format(table_name))
            if headers == None:
                cursor.copy_from(ioContent, table_name)
            else:
                cursor.copy_from(ioContent, table_name, columns=headers)
            connection.commit()
            self.__callSuccessEvent(table_name, file_path)
        except Exception as error:
            logging.error("Error migrating table: {table_name}. File: {} Exception:{}".format(
                table_name, file_path, error))
            self.__callFailedEvent(table_name, file_path, error)
        finally:
            cursor.close()
            connection.close()

    def _getRequestRegistered(self,request_name):
         query = "SELECT file_name FROM package_files_loaded where file_name = '{}' and status != '{}'".format(request_name,'outdated')
         return  self.select(query)

    def __callSuccessEvent(self, table_name, file_path):
        try:
            eventFunction = getattr(self, "{}_success".format(table_name))
            eventFunction(table_name, file_path)
        except AttributeError:
            self.success(table_name, file_path)

    def __callFailedEvent(self, table_name, file_path, error):
        try:
            eventFunction = getattr(self, "{}_failed".format(table_name))
            eventFunction(table_name, file_path, error)
        except AttributeError:
            self.failed(table_name, file_path, error)