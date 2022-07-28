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
        self.create_tables()

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
                                CREATE TABLE IF NOT EXISTS user_data(
                                id integer PRIMARY KEY, 
                                user_first_name varchar(300), 
                                user_second_name varchar(300));
                                """)
        sel = self.connection.execute("""
                                CREATE TABLE IF NOT EXISTS candidates(
                                user_id INTEGER REFERENCES user_data(id), 
                                candidate_id INTEGER, in_favorites BOOL);
                                """)
        return sel

    def add_user(self, user_id, first_name: str, last_name: str):
        """
        Add client to DataBase
        :param user_id:
        :param first_name:
        :param last_name:
        :return:
        """
        sel = ()
        try:
            sel = self.connection.execute(
                f"""INSERT INTO user_data VALUES (
                            '{user_id}', 
                            '{self.normalize_user_data(first_name)}', 
                            '{self.normalize_user_data(last_name)}');"""
            )
        except sqlalchemy.exc.IntegrityError:
            print('This person was in DataBae yet.')
        return sel

    def add_candidate(self, user_id, candidate_id, in_favorites=False):
        """
        Add a candidate to DataBase
        :param user_id:
        :param candidate_id:
        :param in_favorites:
        :return:
        """
        sel = ()
        try:
            sel = self.connection.execute(
                f"""INSERT INTO candidates VALUES (
                        '{user_id}', 
                        '{candidate_id}', 
                        '{in_favorites}');"""
            )
        except sqlalchemy.exc.IntegrityError:
            print('This person was in DataBae yet.')
        return sel

    def check_candidate(self, user_id, candidate_id):
        sel = self.connection.execute(f"""SELECT EXISTS(SELECT * FROM candidates
                    WHERE user_id = '{user_id}' AND candidate_id ={candidate_id});"""
                                      ).fetchall()
        return sel[0][0]
