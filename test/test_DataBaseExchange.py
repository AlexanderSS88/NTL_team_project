import unittest
from parameterized import parameterized

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
