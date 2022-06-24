from sqlite3 import Cursor
from unittest import result
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import itertools

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def add_user(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = '''
        INSERT INTO `user` (`id`, `username`, `password`) VALUES (NULL, '{}', '{}');
        '''.format(username, password)
        cursor.execute(sql)
        self.connection.commit()
        new_row = cursor.lastrowid
        return new_row
        
    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "SELECT * from user where username = '{}'".format(username)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            cursor.close()
            return 0
        else:
            resultfetch = cursor.fetchone()
            if(resultfetch['password'] == password):
                cursor.close()
                return 1
            else:
                cursor.close()
                return 0

    def get_news(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM news WHERE uploadDate >= DATE_SUB(curdate(), INTERVAL 30 DAY)"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            rows = []
        cursor.close()
        return rows
    
    def get_news_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM news WHERE id = {}".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def post(self, news):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = '''
        INSERT INTO news (content, uploadDate) VALUES ('{}', CURRENT_DATE)
        '''.format(news)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return 'News added'
    
    def edit(self, content, id):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = '''
        UPDATE `news` SET `content` = '{}', uploadDate = CURRENT_DATE WHERE `news`.`id` = {};
        '''.format(content, id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()      
        return 'Edit Succesful'
    
    def delete(self, id):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        sql = "DELETE FROM news WHERE id = {}".format(id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return 'News Deleted'
    
    def __del__(self):
        self.connection.close()


class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='news_board',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())