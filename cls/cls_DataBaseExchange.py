import sqlalchemy
import re
from cls.cls_DataBaseConnection import DataBaseConnection

"""
Here collected all dialogs between program and database.
"""


class DataBaseExchange(DataBaseConnection):

    def __init__(self, db_data_file_path='/tokens/application_data.ini', make_connection=True):
        super().__init__(make_connection=make_connection, db_data_file_path=db_data_file_path)

    def add_user_data(self, user_data: dict):
        """
        Add a user data to database
        :param user_data:
        :return: None
        """

        sel = self.connection.execute(
            f"SELECT EXISTS(SELECT * FROM user_info WHERE id={user_data.get('id')});").fetchmany(1)

        if sel[0][0]:
            print('This person was in DataBase. Personal data will be rewritten.')
            self.connection.execute(f"DELETE FROM user_info WHERE id={user_data.get('id')};")

        try:
            self.connection.execute(
                f"""INSERT INTO user_info VALUES (
                '{user_data.get('id')}', 
                '{self.normalize_user_data(user_data.get('first_name'))}', 
                '{self.normalize_user_data(user_data.get('last_name'))}', 
                '{user_data.get('age')}', 
                '{user_data.get('sex')}', 
                '{self.normalize_user_data(user_data.get('city'))}', 
                '{user_data.get('url')}');"""
            )
            print(f"User {user_data.get('id')} data recorded to DataBae.")
        except sqlalchemy.exc.IntegrityError:
            print('This person was in DataBae yet.')

    @staticmethod
    def normalize_user_data(data_str):
        """
        Solve some word problems before add data to database.
        :param data_str:
        :return: fixed string
        """
        return re.sub("[$|@|&|'|*]", "", data_str)

    def create_tables(self):
        """
        Create tables in database if there is are not existed
        """
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

    def get_candidates(self, min_age: int, max_age: int, city_name: str) -> list:

        if min_age == max_age:
            return [item[0] for item in self.connection.execute(
                f"""SELECT id FROM user_info WHERE
                        age = {min_age}
                        AND city = '{city_name}';""").fetchall()]
        else:
            return [item[0] for item in self.connection.execute(
                f"""SELECT id FROM user_info WHERE
                age BETWEEN {min_age} AND {max_age}
                AND city = '{city_name}';""").fetchall()]
