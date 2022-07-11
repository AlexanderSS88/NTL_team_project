import pathlib
from pathlib import Path
import configparser
import sqlalchemy

"""
Here program takes database parameters from configuration file and make connection.
"""
class DataBaseConnection:
    def __init__(self, make_connection: bool, db_data_file_path='/tokens/database_data.txt'):
        # it's not necessary to make database connections in some tests
        if make_connection:
            self.connection = self.make_database_connection(db_data_file_path)
            print(self.connection)

    @staticmethod
    def make_database_connection(db_data_file_path: str):
        path = str(Path(pathlib.Path.cwd())) + db_data_file_path

        print(path)

        config = configparser.ConfigParser()
        config.read(path)

        user_name = config['DEFAULT']['user_name']
        user_pass_word = config['DEFAULT']['user_pass_word']
        port = config['DEFAULT']['port']
        database_name = config['DEFAULT']['database_name']
        host = config['DEFAULT']['host']

        engine = sqlalchemy.create_engine(
            f'postgresql://{user_name}:{user_pass_word}@{host}:{port}/{database_name}')

        return engine.connect()
