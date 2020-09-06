from database import Database
from random import randint
from datetime import datetime
import psycopg2


# enter correct details here
db_host = ''
db_port = 10467
db_username = ''
db_password = ''


def test_create_db():    
    db_name = 'testdb_{0}'.format(randint(0, 100))
    database = Database(db_host, db_port, db_name, db_username, db_password)   

    db_conn = psycopg2.connect('postgres://{0}:{1}@{2}:{3}/{4}?sslmode=require'.format(db_username, db_password, db_host, db_port, db_name))
    cursor = db_conn.cursor()
    cursor.execute('select datname FROM pg_database;')
    rows = cursor.fetchall()    
    databases = [row[0] for row in rows]

    query = "SELECT table_name FROM information_schema.tables WHERE (table_schema = 'public') ORDER BY table_schema, table_name;"
    cursor.execute(query)
    table_rows = cursor.fetchall()
    tables = [row[0] for row in table_rows]
    database.drop_database(db_name)
    assert db_name in databases
    assert 'Monitor' in tables


def test_write_data():
    data = {
        'site': 'test_site_1',
        'httpcode': 200,
        'duration': 0.0132524352,
        'pattern': 'NOT_FOUND',
        'error': None,
        'history': '308',
        'timestamp': datetime.now()
    }
    db_name = 'testdb_{0}'.format(randint(0, 100))
    database = Database(db_host, db_port, db_name, db_username, db_password)   
    database.write_data(
        data['site'],
        data['httpcode'],
        data['duration'],
        data['pattern'],
        data['error'],
        data['history'],
        data['timestamp']
    )
    db_conn = psycopg2.connect('postgres://{0}:{1}@{2}:{3}/{4}?sslmode=require'.format(db_username, db_password, db_host, db_port, db_name))
    cursor = db_conn.cursor()
    cursor.execute('select site, httpcode, duration, pattern, error, history, timestamp from "Monitor";')
    record = cursor.fetchone()    
    database.drop_database(db_name)

    assert record[0] == data['site']
    assert record[1] == data['httpcode']
    assert record[2] == data['duration']
    assert record[3] == data['pattern']
    assert record[4] == data['error']
    assert record[5] == data['history']
    assert record[6] == data['timestamp']
