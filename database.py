import psycopg2 as pg
from sqlalchemy import create_engine

# This class will manage the communication with the Postgres database
class DatabaseConnector:
    # Constructor of the class 
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        
    # Connection to the Postgres database 
    def connect(self):
        try:
            self.connection = pg.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Connection successful!")
        except pg.Error as e:
            print(f"Error connecting to the database: {e}")

    # Disconnect from the Postgres database
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            print("Connection closed.")

    # Given the city name as input, returns the id from City table
    def select_id_from_city(self, city_name):
        try:
            cursor = self.connection.cursor()

            # Create the SQL query for selecting the ID
            table = '"City"'
            query = f"SELECT id FROM {table} WHERE city_name LIKE '%{city_name}%'"

            # Execute the select query
            cursor.execute(query)

            # Fetch the city ID value
            result = cursor.fetchone()

            if result is not None:
                idCity = result[0]
            else:
                idCity = 0
                print("No matching ID found.")
        except pg.Error as e:
            idCity = 0
            print(f"Error selecting ID from the table: {e}")
        finally:
            cursor.close()
            return idCity
            
    # Given the table name and DataFrame as input, insert the data from DataFrame to the destination table
    def insert_data_from_dataframe(self, dest_table, source_df):
        # Construct the database URL
        db_url = f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'

        # Create a SQLAlchemy engine
        engine = create_engine(db_url)
        
        try:
            # Insert the DataFrame into the table using SQLAlchemy engine
            # Note: SQLAlchemy engine has been used to simplify the loading process
            source_df.to_sql(dest_table, engine, if_exists="append", index=False)
            print(f"Data successfully written into Database.")
        except Exception as e:
            print(f"An error occurred while writing to {dest_table} table: {e}")
        
        # Dispose the engine
        engine.dispose()
