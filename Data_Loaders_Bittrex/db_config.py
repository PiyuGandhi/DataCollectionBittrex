database_credentials = {
    'user': 'postgres',
    'host': 'localhost',
    'dbname': 'forex_data',
    'password': 'assignment123',
    'port': 5432
}


min_data_query = """create table min{}_data (
"Timestamp" timestamp,
"Symbol" text,
"Open" decimal,
"High" decimal,
"Low" decimal,
"Close" decimal,
"Volume" decimal
)"""

min_data_columns = ["Timestamp", "Symbol", "Open", "High", "Low", "Close", "Volume"]