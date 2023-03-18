import psycopg2
import logging
import time, datetime
import os
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, LOG_LEVEL

class PgAPI:

    permission = None

    def __init__(self):
        self.connection = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST)
        self._createPermissionTable()

    #Создание таблиц
    def __tableCreate__(self, sql):
        try:
            cursor = self.connection.cursor()
            cursor.execute("ROLLBACK")
            cursor.execute(sql)
            self.connection.commit()
            logging.debug("DB created SUCCESS")
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f"{error}")
        finally:
            if self.connection:
                cursor.close()

    #INSERT в таблицу
    def __tableInsert__(self, sql):
        result = None

        try:
            cursor = self.connection.cursor()
            cursor.execute("ROLLBACK")
            cursor.execute(sql)
            self.connection.commit()
            logging.debug('DB inserted SUCCESS')
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f"{error}")
        finally:
            if self.connection:
                cursor.close()
        return result

    # UPDATE в таблицу
    def __tableUpdate__(self, sql):
        result = None

        try:
            cursor = self.connection.cursor()
            cursor.execute("ROLLBACK")
            cursor.execute(sql)
            self.connection.commit()
            logging.debug('DB update SUCCESS')
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f"{error}")
        finally:
            if self.connection:
                cursor.close()
        return result

    #SELECT из таблицы
    def __tableSelect__(self, sql):

        result = None

        try:
            cursor = self.connection.cursor()
            cursor.execute("ROLLBACK")
            cursor.execute(sql)
            result = cursor.fetchall()
            logging.debug('DB select SUCCESS')
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f"{error}")
        finally:
            if self.connection:
                cursor.close()
        return result

    # Создание таблицы Permission
    def _createPermissionTable(self):

        sql = '''CREATE TABLE permission (
                id              SERIAL PRIMARY KEY,
                permission	    integer,
                first_name      varchar(60),
                last_name       varchar(60),
                user_id         bigint UNIQUE,
                created         bigint NOT NULL,
                changed         bigint NOT NULL
                  );'''
        self.__tableCreate__(sql)

    def _insertPermissionMember(self, memberInfo):
        sql = f"""
                INSERT INTO permission (permission, first_name, last_name, user_id, created, changed)
                VALUES (
                0,
                '{memberInfo.get('first_name')}',
                '{memberInfo.get('last_name')}',
                '{memberInfo.get('user_id')}',
                {int(time.time())},
                {int(time.time())}
                )
                """
        self.__tableInsert__(sql)

    def getMemberPermission(self, user_id):
        sql = f"SELECT permission FROM permission WHERE user_id = {user_id}"
        result = self.__tableSelect__(sql)
        result = result[0][0]
        return result

    def getCreatedOrders(self):
        sql = f"SELECT * FROM orders WHERE status = 'CREATED' ORDER BY created"
        text = ""
        results = self.__tableSelect__(sql)
        if results.__len__() > 0:
            for result in results:
                result = list(result)
                text += f"id: {result[0]}\n" \
                        f"Пара: {result[1]}\n" \
                        f"Тип: {result[7]}\n" \
                        f"Цена: {result[2]}\n" \
                        f"Кол-во: {result[3]}\n" \
                        f"Сумма + ком: {result[6]}\n" \
                        f"Дата: {datetime.datetime.fromtimestamp(result[9])}\n" \
                        f"\n"
        else:
            text += "0 записей"
        return text

    def getFinishedOrders(self):
        sql = f"SELECT * FROM orders WHERE status = 'FINISHED' ORDER BY created"
        text = ""
        results = self.__tableSelect__(sql)
        if results.__len__() > 0:
            for result in results:
                result = list(result)
                text += f"id: {result[0]}\n" \
                        f"Пара: {result[1]}\n" \
                        f"Тип: {result[7]}\n" \
                        f"Цена: {result[2]}\n" \
                        f"Кол-во: {result[3]}\n" \
                        f"Сумма + ком: {result[6]}\n" \
                        f"Дата: {datetime.datetime.fromtimestamp(result[9])}\n" \
                        f"\n"
        else:
            text += "0 записей"
        return text

    def getMembersInfo(self):
        sql = f"SELECT * FROM permission ORDER BY created"
        text = ""
        results = self.__tableSelect__(sql)
        if results.__len__() > 0:
            for result in results:
                result = list(result)
                perm = ""
                if result[1] == 1000:
                    perm = "ADMIN"
                else:
                    perm = "USER"

                text += f"Имя:  {result[2]} {result[3]}\n" \
                        f"Права:  {perm}\n" \
                        f"ID:  {result[4]}\n" \
                        f"Дата:  {datetime.datetime.fromtimestamp(result[5])}\n" \
                        f"\n"
        else:
            text += "0 записей"
        return text

    def getPairsInfo(self, pairs):
        sql = f"SELECT * FROM pairs WHERE pairs ='{pairs}'"
        return self.__tableSelect__(sql)


    def getLogInfo(self, deep):
        file = os.path.join(os.path.dirname(__file__), '..', 'YobitTrader', 'YobitTrader.log')
        content = open(file, "r")
        lines = content.readlines()
        content.close()
        i = lines.__len__() - deep
        text = ""

        while i < lines.__len__():
            text += lines[i]
            i += 1

        return text