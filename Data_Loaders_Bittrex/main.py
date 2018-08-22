import psycopg2
from Data_Loaders_Bittrex.db_utils2 import *
from Data_Loaders_Bittrex.data_loaders import *
import time


def check_connection():
    try:
        db_connection = psycopg2.connect(database=database_credentials['dbname'])
        db_connection.close()
    except psycopg2.OperationalError as err:
        create_forex_data_db()
        for i in [1, 5, 15, 30, 60]:
            create_table(i)


def main():
    DL = DataLoader()
    data = DL.get_all_ticks_data()
    write_data_to_db(data, time_frame=1)
    return data


t0 = time.time()
whole_data = None

while True:
    DL = DataLoader()
    try:
        check_connection()
        if whole_data is None:
            whole_data = main()
        else:
            whole_data.append(main())

        for timeperiod in [5, 15, 30, 60]:
            if (time.time() - t0) == 60*timeperiod:
                min_data = DL.resample_data(whole_data, timeperiod)
                write_data_to_db(min_data, time_frame=timeperiod)

            if timeperiod == 60:
                t0 = time.time()
                whole_data = None


    except Exception as e:
        print(e)
        continue