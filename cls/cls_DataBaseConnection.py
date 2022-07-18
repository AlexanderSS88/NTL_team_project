import pathlib
from pathlib import Path
import sqlalchemy
from tokens.cls_tokens import Token

"""
Here program takes database parameters from configuration file and make connection.
"""


class mkConnection:
    def execute(self, message):
        return message


class DataBaseConnection:
    connection = mkConnection()

    def __init__(self, make_connection: bool, db_data_file_path='tokens'):
        self.db_data_file_path = db_data_file_path
        # it's not necessary to make database connections in some tests
        if make_connection:
            engine = sqlalchemy.create_engine(self.prepare_database_connection())

            self.connection = engine.connect()

            # print(f'type(self.connection): {type(self.connection)}')
            #
            # print(self.connection)

    def prepare_database_connection(self):
        token = Token(self.db_data_file_path)

        user_name = token.app_dict['DATABASE']['user_name']
        port = token.app_dict['DATABASE']['port']
        database_name = token.app_dict['DATABASE']['database_name']
        host = token.app_dict['DATABASE']['host']
        user_pass_word = token.app_dict['PASSWORDS']['db_passw']

        return f'postgresql://{user_name}:{user_pass_word}@{host}:{port}/{database_name}'
