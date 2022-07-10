import sqlalchemy
import pathlib
from pathlib import Path
import configparser


class DataBaseExchange:

    def __init__(self, db_data_file_path='/tokens/database_data.txt'):
        self.connection = self.make_database_connection(db_data_file_path)

        print(self.connection)

    def make_database_connection(self, db_data_file_path: str):
        path = str(Path(pathlib.Path.cwd())) + db_data_file_path

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

    """
                {'first_name': self.pers_data_json['response'][0]['first_name'],
                    'last_name': self.pers_data_json['response'][0]['last_name'],
                    'id': self.user_id,
                    'url': f'https://vk.com/id{self.user_id}',
                    'age': self.age,
                    'city': self.city_name,
                    'city_id': self.city_id,
                    'interests': self.interests,
                    'photos_list': self.photo_list}
    """

    def add_user_data(self, user_data: dict):
        ...

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
