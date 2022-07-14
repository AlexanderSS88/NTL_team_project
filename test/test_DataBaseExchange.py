import unittest
from parameterized import parameterized
from tokens.cls_tokens import Token

from cls.cls_DataBaseExchange import DataBaseExchange


class TestDBFunctions(unittest.TestCase):

    @parameterized.expand(
        [
            ('Иванов', 'Иванов'),
            ("Bdf'dfr", "Bdfdfr"),
            ("Ёжиокв*", "Ёжиокв"),
            ("Ёжиокв'", "Ёжиокв")
        ]
    )
    def test_normalize_user_data(self, data_str, result):
        db = DataBaseExchange(make_connection=False)
        self.assertMultiLineEqual(db.normalize_user_data(data_str), result)

    def test_prepare_database_connection(self):
        db = DataBaseExchange(make_connection=False, db_data_file_path='tokens_4_test')
        self.assertMultiLineEqual(db.prepare_database_connection(),
                                  f'postgresql://postgres:password@localhost:5432/cours_w_DB')



