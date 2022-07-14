import unittest
from unittest import mock
from pprint import pprint

from vk_tools.cls_VkUrl import VkUrl


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    print(f'args[0]:\t{args[0]}')
    pprint(f'kwargs: {kwargs}')

    if args[0] == 'https://api.vk.com/method/users.get' \
            and kwargs['params'] == '&access_token=vk_token&v=5.81&fields=bdate,sex,city,interests,music&user_ids=125':
        return MockResponse({"response": "value1"}, 200)
    elif args[0] == 'https://api.vk.com/method/photos.get' \
            and kwargs[
        'params'] == '&access_token=vk_token&v=5.81&fields=&owner_id=125&album_id=profile&count=200&photo_sizes' \
                     '=1&extended=1':
        return MockResponse({"response": {"items": "value2"}}, 200)
    elif args[0] == 'https://api.vk.com/method/photos.getAlbums' \
            and kwargs['params'] == '&access_token=vk_token&v=5.81&fields=&owner_id=125':
        return MockResponse({'response': {'items': [{'id': 1000}]}}, 200)

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

    @mock.patch('vk_tools.cls_VkUrl.requests.get', side_effect=mocked_requests_get)
    def test_get_personal_data(self, mock_get):
        json_data = self.vk.get_personal_data('125')
        print(f'json_data: {json_data}')
        self.assertEqual(json_data, {"response": "value1"})

    @mock.patch('vk_tools.cls_VkUrl.requests.get', side_effect=mocked_requests_get)
    def test_get_photo_f_profile(self, mock_get):
        json_data = self.vk.get_photo_f_profile('125', 'profile')
        print(f'json_data2: {json_data}')
        self.assertEqual(json_data, "value2")

    @mock.patch('vk_tools.cls_VkUrl.requests.get', side_effect=mocked_requests_get)
    def test_get_photo_f_profile_by_album_list(self, mock_get):
        json_data = self.vk.get_photo_f_profile_by_album_list('125', ['profile'])
        print(f'json_data2: {json_data}')
        self.assertListEqual(json_data, ["value2"])

    @mock.patch('vk_tools.cls_VkUrl.requests.get', side_effect=mocked_requests_get)
    def test_search_albums(self, mock_get):
        json_data = self.vk.search_albums('125')
        print(f'json_data2: {json_data}')
        self.assertListEqual(json_data, [1000])
