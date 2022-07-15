import unittest
from parameterized import parameterized

from cls.cls_DataBaseExchange import DataBaseExchange


class TestDBFunctions(unittest.TestCase):

    def setUp(self):
        self.db = DataBaseExchange(make_connection=False, db_data_file_path='tokens_4_test')

    @parameterized.expand(
        [
            ('Иванов', 'Иванов'),
            ("Bdf'dfr", "Bdfdfr"),
            ("Ёжиокв*", "Ёжиокв"),
            ("Ёжиокв'", "Ёжиокв")
        ]
    )
    def test_normalize_user_data(self, data_str, result):
        self.assertMultiLineEqual(self.db.normalize_user_data(data_str), result)

    def test_prepare_database_connection(self):
        self.assertMultiLineEqual(self.db.prepare_database_connection(),
                                  f'postgresql://postgres:password@localhost:5432/cours_w_DB')

    def test_connection(self):
        self.assertMultiLineEqual(self.db.connection.execute('execute'), 'execute')

    @parameterized.expand(
        [({'id': '1',
         'first_name': 'Иван',
         'last_name': 'Иванов',
         'age': '25',
         'sex': '2',
         'city': 'Ёбург',
         'url': 'https://vk.com/id1'},
          """INSERT INTO user_info VALUES (
                '1', 
                'Иван', 
                'Иванов', 
                '25', 
                '2', 
                'Ёбург', 
                'https://vk.com/id1');"""
          ),
         ({'id': '1',
           'first_name': '$Иван$',
           'last_name': '@Иванов@',
           'age': '25',
           'sex': '2',
           'city': "Ё'бург&",
           'url': 'https://vk.com/id1'},
          """INSERT INTO user_info VALUES (
                '1', 
                'Иван', 
                'Иванов', 
                '25', 
                '2', 
                'Ёбург', 
                'https://vk.com/id1');"""
          )
         ]
     )
    def test_add_user_data(self, user_dict, result):
        self.assertMultiLineEqual(self.db.add_user_data(user_dict), result)
