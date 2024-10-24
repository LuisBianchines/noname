import pyodbc
import configparser
import psycopg2
from datetime import date, datetime
import logging
import base64

# Definindo constantes
SQLSERVER = 'SQLSERVER'
PG = 'PG'

class Connection():
    __host = None
    __database = None
    __user_db = None    
    __password = None   
    __db_type = None 
    __connected = None
    __port = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        print(config.sections())

        Connection.__host = config.get('DATABASE', 'HOST')
        Connection.__database = config.get('DATABASE', 'DATABASE')
        Connection.__user_db = config.get('DATABASE', 'USER_BD')
        Connection.__password = config.get('DATABASE', 'PASSWORD') 
        Connection.__db_type = config.get('DATABASE', 'DB_TYPE')
        Connection.__port = config.get('DATABASE', 'PORT')
        Connection.__connected = False
        Connection.conn = None
        Connection.cursor = None

    @staticmethod
    def connect():    
        if Connection.__db_type == SQLSERVER:
            logging.info('Conectando ao SQL Server...')
            try:
                Connection.conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=' + Connection.__host + ';'
                    'DATABASE=' + Connection.__database + ';'
                    'UID=' + Connection.__user_db + ';'
                    'PWD=' + Connection.__password + ';'
                )
                Connection.cursor = Connection.conn.cursor()
                Connection.__connected = True
            except Exception as e:
                logging.error(e)
                raise
        else:
            logging.info('Conectando ao PG...')
            try:
                Connection.conn = psycopg2.connect(host=Connection.__host,
                                                   database=Connection.__database,
                                                   user=Connection.__user_db,
                                                   password=Connection.__password,
                                                   port=Connection.__port)

                Connection.cursor = Connection.conn.cursor()
                Connection.__connected = True
            except Exception as error:
                logging.error(error)
                raise

    @staticmethod            
    def open_query_to_json(query):
        Connection.cursor.execute(query)
        return Connection.to_json()        

    def open_query_param_to_json(query, params):
        Connection.cursor.execute(query, (params))
        return Connection.to_json()    

    def update (query, data): 
        try:
           Connection.cursor.execute(query, data)
           Connection.conn.commit() 
           return 'updated', True
        except (Exception, psycopg2.DatabaseError) as error:
            Connection.conn.rollback()
            logging.error(error.diag.message_primary)
            return error.diag.message_primary, False
        
    def delete (query, data): 
        try:
           Connection.cursor.execute(query, data)
           Connection.conn.commit() 
           return 'updated', True
        except (Exception, psycopg2.DatabaseError) as error:
            Connection.conn.rollback()
            logging.error(error.diag.message_primary)
            return error.diag.message_primary, False    
    
    @staticmethod    
    def execute( query): 
        try:
           Connection.cursor.execute(query)
           Connection.conn.commit() 
           return 'executed', True
        except (Exception, psycopg2.DatabaseError) as error:
            Connection.conn.rollback()
            logging.error(error.diag.message_primary)
            return error.diag.message_primary, False

    def insert( query, data): 
        try:
           Connection.cursor.execute(query, data)
           Connection.conn.commit() 
           return 'created', True
        except (Exception, psycopg2.DatabaseError) as error:
            Connection.conn.rollback()
            logging.error(error.diag.message_primary)
            return error.diag.message_primary, False

    def to_json():
        columns = [col[0] for col in Connection.cursor.description]
        
        _data = []
        
        for row in Connection.cursor.fetchall():
            formatted_row = {}
            for col, value in zip(columns, row):
                if isinstance(value, bytes):  # Check if the value is bytes
                    formatted_row[col] = base64.b64encode(value).decode()  # Convert bytes to base64 string
                elif (isinstance(value, date)) or (isinstance(value, datetime)):
                    formatted_row[col] = value.isoformat()
                else:
                    formatted_row[col] = value   
                    
            _data.append(formatted_row)

        return _data
    
    def delete(query, data):
        try:
            Connection.cursor.execute(query, data)
            Connection.conn.commit()
            return 'deleted', True
        except (Exception, psycopg2.DatabaseError) as error:
            Connection.conn.rollback()
            logging.error(error.diag.message_primary)
            return error.diag.message_primary, False
    