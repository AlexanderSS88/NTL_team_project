import sqlalchemy
import pathlib
from pathlib import Path
import configparser  # импортируем библиотеку


class DataBaseExchange:

    # def __init__(self, db_info='postgresql://postgres:vrag@localhost:5432/courcr_w_DB'):
    def __init__(self, db_data_file_path='/tokens/database_data.txt'):
        self.connection = self.make_database_connection(db_data_file_path)

        print(self.connection)

    def make_database_connection(self, db_data_file_path: str):

        path = str(Path(pathlib.Path.cwd())) + db_data_file_path
        print(pathlib.Path.cwd())
        print(path)


        config = configparser.ConfigParser()  # create a parser object
        print(path)
        print(config.read(path))  # read confif file

        # # print(config)
        # print(len(config))
        # print(config['DEFAULT'])
        #
        # for key, val in config['DEFAULT'].items():
        #     print(f'{key}: {val}')
        #
        # user_name = config['DEFAULT']['user_name']
        # user_pass_word = config['DEFAULT']['user_pass_word']
        # port = config['DEFAULT']['port']
        # database_name = config['DEFAULT']['database_name']
        # host = config['DEFAULT']['host']
        #
        # # engine = sqlalchemy.create_engine('postgresql://postgres:vrag@localhost:5432/cours_w_DB')
        #
        # engine = sqlalchemy.create_engine(
        #     f'postgresql://{user_name}:{user_pass_word}@{host}:{port}/{database_name}')
        #
        # engine = sqlalchemy.create_engine(
        #     f'postgresql://{user_name}:{user_pass_word}@{host}:{port}/{database_name}')
        #
        # return engine.connect()

        return None



    def create_tables(self):
        sel = self.connection.execute("""
        CREATE TABLE IF NOT EXISTS user_info (
        id integer PRIMARY KEY,
        user_name varchar(40) NOT NULL,
        user_surname varchar(40) NOT NULL,
        age int,
        sex int,
        city varchar (40),
        account_link varchar(80) NOT NULL
        );
        """)
        print(sel)

        sel = self.connection.execute("""CREATE TABLE IF NOT EXISTS photos (
        id integer PRIMARY KEY,
        photo_link varchar(300),
        photo_id_user integer REFERENCES user_info(id)
        );
        """)
        print(sel)

        sel = self.connection.execute("""
        CREATE TABLE IF NOT EXISTS interests(
        id integer PRIMARY KEY,
        interest_name varchar(40) NOT NULL,
        interest_id_user integer REFERENCES user_info(id)
        );
        """)
        print(sel)
