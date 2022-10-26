import pymysql
import pymysql.cursors
import logging
from config.DatabaseConfig import *

class Database:
    '''
    데이터 베이스 제어
    '''

    def __init__(self):
        self.host= '127.0.0.1'
        self.user= 'root'
        self.password='19791127'
        self.db_name = 'wbti'
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database =self.db_name )
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        print('DB에 성공적으로 연결되었습니다. ')

    def close(self):
        self.conn.close()
        print('DB 연결을 끊었습니다.')

    def getConnection(self):
        self.conn.ping()
        return self.conn, self.cur

    def execute(self, sql):
        last_row_id = -1
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
            self.conn.commit()
            last_row_id = cursor.lastrowid
            result = cursor.fetchall()

        except Exception as ex:
            logging.error(ex)

        finally:
            return result

    def select_one(self,sql):
        result = None

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
        except Exception as ex:
            logging.error(ex)

        finally:
            return result

    def select_all(self, sql):
        result= None
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        except Exception as ex:
            logging.error(ex)

        finally:
            return result

