import unittest
import requests
from unittest import mock
from parameterized import parameterized

from vk_tools.cls_VkUrl import VkUrl

# This is the class we want to test
class MyGreatClass:
    def fetch_json(self, url):
        response = requests.get(url)
        return response.json()


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    print(f'args[0]:\t{args[0]}')

    if args[0] == 'https://api.vk.com/method/users.get':
        return MockResponse({"key1": "value1"}, 200)
    elif args[0] == 'http://someotherurl.com/anothertest.json':
        return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)


class TestVKFunctions(unittest.TestCase):
    vk = VkUrl(db_data_file_path='tokens_4_test')

    def test_get_url(self):
        self.assertMultiLineEqual(self.vk.get_url('users.get'), "https://api.vk.com/method/users.get")

    def test_get_params(self):
        self.assertDictEqual(self.vk.get_params(fields='bdate,city',
                                                pdict={'user_ids': '125'}), {'access_token': 'vk_token',
                                                                             'v': '5.81',
                                                                             'fields': 'bdate,city',
                                                                             'user_ids': '125'})

    def test_transform_param(self):
        self.assertMultiLineEqual(self.vk.transform_param({'access_token': 'vk_token',
                                                           'v': '5.81',
                                                           'fields': 'bdate,city',
                                                           'user_ids': '125'}),
                                  '&access_token=vk_token&v=5.81&fields=bdate,city&user_ids=125')

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('vk_tools.cls_VkUrl.requests.get', side_effect=mocked_requests_get)
    # @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_base_personal_data(self, mock_get):
        # mgc = MyGreatClass()
        # json_data = mgc.fetch_json('http://someotherurl.com/anothertest.json')
        # self.assertEqual(json_data, {"key2": "value2"})
        json_data = self.vk.get_base_personal_data('125')
        print(f'json_data: {json_data}')
        # "https://api.vk.com/method/users.get&&access_token=vk_token&v=5.81&fields=bdate,city&user_ids=125"
        self.assertEqual(json_data, {"key1": "value1"})

