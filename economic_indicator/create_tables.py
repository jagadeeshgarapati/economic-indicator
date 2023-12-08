import psycopg2

from economic_indicator.database import connect_db


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        "CREATE TABLE IF NOT EXISTS economic_indicators ("
        "country_code VARCHAR(2),year INTEGER,"
        "gdp_growth_rate FLOAT,"
        "population_growth_rate FLOAT,"
        "gni_per_capita FLOAT,"
        "inflation_rate FLOAT,"
        "government_debt FLOAT,"
        "fdi_net_inflows FLOAT,"
        "ease_of_doing_business FLOAT,"
        "export_percent_gdp FLOAT,"
        "import_percent_gdp FLOAT,"
        "PRIMARY KEY (country_code, year)"
        ")",
        )
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
            # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()