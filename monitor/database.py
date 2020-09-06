from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2


class Database():
    def __init__(self, host, port, name, username, password):
        self.host = host
        self.port = port
        self.dbname = name
        self.username = username
        self.password = password

        self.create_database(self.dbname)
        self.create_table('Monitor')

    def create_database(self, db_name):
        try:
            conn = psycopg2.connect('postgres://{0}:{1}@{2}:{3}/{4}?sslmode=require'.format(self.username, self.password, self.host, self.port, 'defaultdb'))
            cursor = conn.cursor()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # create database
            query = 'CREATE database {0};'.format(db_name)
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            print(ex)


    def drop_database(self, db_name):
        try:
            conn = psycopg2.connect('postgres://{0}:{1}@{2}:{3}/{4}?sslmode=require'.format(self.username, self.password, self.host, self.port, 'defaultdb'))
            cursor = conn.cursor()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # drop database
            query = 'DROP database if exists {0}'.format(db_name)
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            print(ex)


    def create_table(self, table_name):
        try:
            conn = psycopg2.connect('postgres://{0}:{1}@{2}:{3}/{4}?sslmode=require'.format(self.username, self.password, self.host, self.port, self.dbname))
            cursor = conn.cursor()
            # create table query
            query = 'CREATE TABLE IF NOT EXISTS "{0}"("id" SERIAL primary key, "site" VARCHAR(50), "httpcode" INT NULL, "duration" double precision, "pattern" VARCHAR(11), "error" VARCHAR(20) NULL, "history" VARCHAR NULL, "timestamp" timestamp);'.format(table_name)
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            print(ex)


    def write_data(self, site, httpcode, duration, pattern, error, history, timestamp):
        try:
            conn = psycopg2.connect('postgres://{0}:{1}@{2}:{3}/{4}?sslmode=require'.format(self.username, self.password, self.host, self.port, self.dbname))
            cursor = conn.cursor()
            # write data to database
            cursor.execute("""
                insert into "Monitor" (site, httpcode, duration, pattern, error, history, timestamp) 
                VALUES (%s,%s,%s,%s,%s,%s,%s);
                """, (site, httpcode, duration, pattern, error, history, timestamp))
            conn.commit()
        except Exception as ex:
            print(ex)
