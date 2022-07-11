import sqlalchemy
import re
from cls.cls_DataBaseConnection import DataBaseConnection


class DataBaseExchange(DataBaseConnection):

    def __init__(self, db_data_file_path='/tokens/database_data.txt', make_connection=True):
        super().__init__(make_connection=make_connection, db_data_file_path=db_data_file_path)

    def add_user_data(self, user_data: dict):

        sel = self.connection.execute(
            f"SELECT EXISTS(SELECT * FROM user_info WHERE id={user_data.get('id')});").fetchmany(1)

        if sel[0][0]:
            print('This person was in DataBase. Personal data will be rewritten.')
            sel = self.connection.execute(f"DELETE FROM user_info WHERE id={user_data.get('id')};")

        try:
            sel = self.connection.execute(f"INSERT INTO user_info VALUES ("
                                          f"'{user_data.get('id')}', "
                                          f"'{self.normalize_user_data(user_data.get('first_name'))}', "
                                          f"'{self.normalize_user_data(user_data.get('last_name'))}', "
                                          f"'{user_data.get('age')}', "
                                          f"'{user_data.get('sex')}', "
                                          f"'{self.normalize_user_data(user_data.get('city'))}', "
                                          f"'{user_data.get('url')}');"
                                          )
            print(f"User {user_data.get('id')} data recorded to DataBae.")
        except sqlalchemy.exc.IntegrityError:
            print('This person was in DataBae yet.')

    @staticmethod
    def normalize_user_data(data_str):
        return re.sub("[$|@|&|'|*]", "", data_str)

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
