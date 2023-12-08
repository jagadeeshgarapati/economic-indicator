import psycopg2


def config():
    return {
        'database': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }


def connect_db():
    # read the connection parameters
    params = config()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    return conn

