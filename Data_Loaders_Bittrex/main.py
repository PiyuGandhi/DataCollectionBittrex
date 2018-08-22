import psycopg2
from Data_Loaders_Bittrex.db_utils2 import *
from Data_Loaders_Bittrex.data_loaders import *

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
    db_connection = connect_db()
    db_cursor = get_cursor(db_connection)
    db_cursor.execute("select * from min1_data")
    all_data = pd.DataFrame(db_cursor.fetchall(), columns=min_data_columns).set_index('Timestamp')
    min5_data = DL.resample_data(all_data, 5)
    min15_data = DL.resample_data(all_data, 15)
    min30_data = DL.resample_data(all_data, 30)
    min60_data = DL.resample_data(all_data, 60)
    write_data_to_db(min5_data, time_frame=5)
    write_data_to_db(min15_data, time_frame=15)
    write_data_to_db(min30_data, time_frame=30)
    write_data_to_db(min60_data, time_frame=60)

check_connection()
main()