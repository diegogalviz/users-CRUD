from psycopg2 import connect


HOST = 'localhost'
PORT = 5432
DBNAME = 'usersdb'
USER = 'postgres'
PASSWORD = 'root'


def get_connection():
    conn = connect(host=HOST, port=PORT, dbname=DBNAME, user=USER, password=PASSWORD)
    return conn