import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from Data_Loaders_Bittrex.db_config import *


def connect_db(dbname=database_credentials['dbname'], dbuser=database_credentials['user'],
               dbhost=database_credentials['host'], dbport=database_credentials['port']):

    """
    :param dbname: Database name (default - taken from db_config file).
    :param dbuser: Database user (default - taken from db_config file).
    :param dbhost: Database host (default - taken from db_config file).
    :param dbport: Database port (default - taken from db_config file).
    :return: A connection to postgres databse with the given (or default) configs.
    """

    db_connection = psycopg2.connect(database=dbname,
                                     user=dbuser,
                                     host=dbhost,
                                     port=dbport)

    db_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return db_connection


def get_cursor(db_connection):

    """
    :param db_connection: Connection to postgres db whose cursor is required.
    :return: A cursor to the database that can perform read/write operations.
    """

    db_cursor = db_connection.cursor()
    return db_cursor


def create_forex_data_db():
    """
    Creating Forex_data database
    :return: None
    """
    db_connection = connect_db(
        'postgres',
        database_credentials['user'],
        database_credentials['host'],
        database_credentials['port']
    )
    db_cursor = get_cursor(db_connection)
    db_cursor.execute("create database " + database_credentials['dbname'])
    db_connection.commit()
    db_connection.close()
    return


def create_table(timestamp=1):
    """
    Creates table of table_name
    :param timestamp: timestamp in minute of stored data
    :return: None
    """
    db_connection = connect_db(
        database_credentials['dbname'],
        database_credentials['user'],
        database_credentials['host'],
        database_credentials['port']
    )

    # cursor to read/write database
    db_cursor = get_cursor(db_connection)

    # Execute the query to add table.
    db_cursor.execute(min_data_query.format(timestamp))
    db_connection.commit()
    db_connection.close()

    return


def write_data_to_db(data, time_frame):
    """
    Writes data to database
    :param data: DataFrame to be written
    :param time_frame: time_frame of given data
    :return: None
    """
    db_connection = connect_db(
        database_credentials['dbname'],
        database_credentials['user'],
        database_credentials['host'],
        database_credentials['port']
    )
    db_cursor = get_cursor(db_connection)

    for idx, row in data.iterrows():
        db_cursor.execute("""
        insert into min{}_data values ('{}','{}','{}','{}','{}','{}','{}')
        """.format(
            time_frame,
            idx,
            row['Symbol'],
            row['Open'],
            row['High'],
            row['Low'],
            row['Close'],
            row['Volume']
        )
        )

    db_connection.commit()
    db_connection.close()

    return