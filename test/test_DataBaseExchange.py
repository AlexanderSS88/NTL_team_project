import unittest
from unittest import mock
from parameterized import parameterized
from tokens.cls_tokens import Token

from cls.cls_DataBaseExchange import DataBaseExchange

# This method will be used by the mock to replace requests.get
def mocked_connection_execute(*args):
    class MockResponse:
        def __init__(self, db_return):
            self.db_return = db_return

        def response(self):
            return self.db_return

    print(f'args:\t{args}')

    if args == "SELECT id FROM user_info WHERE age = 30 AND city = 'Москва';":
        return MockResponse([1, 2])
    # elif args[0] == 'https://api.vk.com/method/photos.get' \
    #         and kwargs[
    #     'params'] == '&access_token=vk_token&v=5.81&fields=&owner_id=125&album_id=profile&count=200&photo_sizes' \
    #                  '=1&extended=1':
    #     return MockResponse({"response": {"items": "value2"}}, 200)
    # elif args[0] == 'https://api.vk.com/method/photos.getAlbums' \
    #         and kwargs['params'] == '&access_token=vk_token&v=5.81&fields=&owner_id=125':
    #     return MockResponse({'response': {'items': [{'id': 1000}]}}, 200)

    return MockResponse(None)


class TestDBFunctions(unittest.TestCase):

    db = DataBaseExchange(make_connection=False, db_data_file_path='tokens_4_test')

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

    # @mock.patch('cls.cls_DataBaseExchange.connection.execute', side_effect=mocked_connection_execute)
    # def test_get_candidates(self, mock_get):
    #     data = self.db.create_tables()
    #     self.assertListEqual(data, [1, 2])




