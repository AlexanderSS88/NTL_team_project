import sqlalchemy
from cls.cls_DataBaseConnection import DataBaseConnection


class DataBaseExchange(DataBaseConnection):

    def __init__(self, db_data_file_path='/tokens/database_data.txt'):
        super().__init__(db_data_file_path)

    def add_user_data(self, user_data: dict):
        try:
            sel = self.connection.execute(f"INSERT INTO user_info VALUES ("
                                          f"'{user_data.get('id')}', "
                                          f"'{user_data.get('first_name')}', "
                                          f"'{user_data.get('last_name')}', "
                                          f"'{user_data.get('age')}', "
                                          f"'{user_data.get('sex')}', "
                                          f"'{user_data.get('city')}', "
                                          f"'{user_data.get('url')}');"
                                          )
            print(f"User {user_data.get('id')} data recorded to DataBae.")
        except sqlalchemy.exc.IntegrityError:
            print('This person was in DataBae yet.')

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
