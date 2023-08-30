import psycopg2
import time, datetime
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

class PostgresAPI:

    def __init__(self):
        self.connection = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST)

    #Создание таблиц
    def __tableCreate__(self, sql):
        try:
            cursor = self.connection.cursor()
            cursor.execute("ROLLBACK")
            cursor.execute(sql)
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"{error}")
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"{error}")
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"{error}")
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"{error}")
        finally:
            if self.connection:
                cursor.close()
        return result

    # Создание таблицы Permission
    def __createPermissionTable__(self):

        sql = '''CREATE TABLE permission (
                id              SERIAL PRIMARY KEY,
                permission      int,
                first_name      varchar(16),
                last_name       varchar(16),
                user_id         bigint NOT NULL,
                created         bigint NOT NULL,
                changed         bigint NOT NULL

                  );'''
        self.__tableCreate__(sql)

    # Добавляем колонку bot в Permission
    def __addBotInPermissionTable__(self):
        sql = '''ALTER TABLE permission ADD COLUMN bot varchar(64);'''
        self.__tableModification__(sql)

    # Создание таблицы Permission
    def __addBotInPermissionTable__(self):
        sql = '''ALTER TABLE permission ADD COLUMN bot varchar(64);'''
        self.__tableUpdate__(sql)

    # Добавить пользователя в подписку
    def setPermission(self, first_name, last_name, user_id, created, changed, bot_key):
        sql = (f"""
                INSERT INTO permission (permission, first_name, last_name, user_id, created, changed, bot) 
                VALUES (
                    0, 
                    '{first_name}', 
                    '{last_name}',
                    {user_id},
                    {created},
                    {changed},
                    '{bot_key}'
                );
            """)
        self.__tableInsert__(sql)

    def getPermissionById(self, user_id, bot_key):
        sql = f"SELECT * FROM permission WHERE user_id = {user_id} AND bot = '{bot_key}'"
        return self.__tableSelect__(sql)

    def getPermissions(self, bot_key):
        sql = f"SELECT * FROM permission WHERE permission = 1000 AND bot = '{bot_key}'"
        return self.__tableSelect__(sql)

    def deletePermissionById(self, user_id, bot_key):
        sql = f"DELETE FROM permission WHERE user_id = '{user_id}' AND bot = '{bot_key}'"
        return self.__tableUpdate__(sql)