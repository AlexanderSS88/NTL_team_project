import sqlalchemy
import re
from cls.cls_DataBaseConnection import DataBaseConnection
from sqlalchemy.exc import IntegrityError

"""Here collected all dialogs between program and database."""


class DataBaseExchange(DataBaseConnection):

    def __init__(self, db_data_file_path='tokens', make_connection=True):
        super().__init__(
                         make_connection=make_connection,
                         db_data_file_path=db_data_file_path
                         )

    def add_user_data(self, user_data: dict):
        """Add a user data to database param:
         user_data: the user data dictionary
        """
        sel = ()
        try:
            sel = self.connection.execute(
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
        return sel

    @staticmethod
    def normalize_user_data(data_str):
        """Solve some word problems before add data to database.
        param data_str:
        return: fixed string
        """
        # return re.sub('[\0\200-\377]', '', data_str)
        return re.sub(r"[$@&'*ó]", "", data_str)

    def create_tables(self):
        """Create tables in database if there is are not existed"""
        self.connection.execute("""
                                CREATE TABLE IF NOT EXISTS user_info 
                                (id integer PRIMARY KEY,
                                user_name varchar(40) NOT NULL,
                                user_surname varchar(40) NOT NULL,
                                age int,
                                sex int,
                                city varchar (40),
                                account_link varchar(80) NOT NULL);
                                """)
        self.connection.execute("""
                                CREATE TABLE IF NOT EXISTS photos 
                                (id integer PRIMARY KEY,
                                photo_link varchar(300),
                                photo_id_user integer REFERENCES user_info(id));
                                """)
        sel = self.connection.execute("""
                                      CREATE TABLE IF NOT EXISTS interests(
                                      id SERIAL PRIMARY KEY,
                                      interest_name varchar(200) NOT NULL,
                                      interest_id_user integer REFERENCES user_info(id));
                                      """)
        return sel

    def get_candidates(self, min_age: int, max_age: int, city_name: str):
        """Get list of candidates identification numbers from DataBase
        by user age and user city param:
        min_age:
        max_age:
        city_name:
        return: list of candidates id
        """
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

    def add_user_photos(self, user_data: dict, photo_list: list, photo_id_list: list):
        """Add a user data to database param:
        user_data: the user data dictionary
        photo_list: list
        photo_id_list: list
        return: Database select request
        """
        sel = ()
        if len(photo_list) > 0:
            for i in range(0, len(photo_list)):
                try:
                    sel = self.connection.execute(
                        f"""INSERT INTO photos VALUES (
                        '{photo_id_list[i - 1]}', 
                        '{photo_list[i - 1]}', 
                        '{user_data.get('id')}');"""
                         )
                    print(f"User photo {i} data recorded to DataBae.")
                except sqlalchemy.exc.IntegrityError:
                    print('This person photo_list in DataBae yet.')
        else:
            print('Error: The photo_list is empty!')
        return sel

    def add_user_interests(self, user_data: dict):
        """Add a user data to database param:
        user_data: the user data dictionary
        return: Database select request
        """
        sel = ()
        for interest in user_data.get('interests'):
            try:
                sel = self.connection.execute(
                    f"""INSERT INTO interests (interest_name, interest_id_user)  VALUES (
                    '{self.normalize_user_data(interest)}', 
                    '{user_data.get('id')}');"""
                     )
                print(f"User {user_data.get('id')} data recorded to DataBae.")
            except sqlalchemy.exc.IntegrityError:
                print('This person data in DataBae yet.')
        return sel

    def get_photo_from_db(self, user_id):
        """Take data of user photoa from DataBase param:
        user_id: user identification number
        return: list_photo_id: list of photos  identification numbers,
        list_photo: list of photos URLs
        """
        sel = [self.connection.execute(
                f"""SELECT id, photo_link FROM photos
                WHERE photo_id_user = '{user_id}';"""
                ).fetchall()
               ]
        list_photo = []
        list_photo_id = []
        for item in sel[0]:
            list_photo_id.append(item[0])
            list_photo.append(item[1])
        return list_photo_id, list_photo
