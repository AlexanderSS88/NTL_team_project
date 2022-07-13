import pathlib
from pathlib import Path
import sqlalchemy
from vk_tools.cls_tokens import Token

"""
Here program takes database parameters from configuration file and make connection.
"""


class DataBaseConnection:
    def __init__(self, make_connection: bool, db_data_file_path='/tokens/application_data.ini'):
        # it's not necessary to make database connections in some tests
        if make_connection:
            self.connection = self.make_database_connection(db_data_file_path)
            print(self.connection)

    @staticmethod
    def make_database_connection(db_data_file_path: str):
        token = Token()

        user_name = token.app_dict['DATABASE']['user_name']
        port = token.app_dict['DATABASE']['port']
        database_name = token.app_dict['DATABASE']['database_name']
        host = token.app_dict['DATABASE']['host']

        path = str(Path(pathlib.Path.cwd())) + '/tokens/db_passw.txt'

        with open(path, 'r') as t_file:
            user_pass_word = t_file.read().strip()

        engine = sqlalchemy.create_engine(
            f'postgresql://{user_name}:{user_pass_word}@{host}:{port}/{database_name}')

        return engine.connect()