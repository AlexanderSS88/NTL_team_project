import requests
import time
from tokens.cls_tokens import Token

from pprint import pprint

"""
This is the VKontakte API communication class
"""


class VkUrl:
    url_ = "https://api.vk.com/method/"

    def __init__(self, db_data_file_path='tokens'):
        token = Token(db_data_file_path)
        self.token = token.app_dict['TOKENS']['vk_token']  # personal token

    def get_url(self, method: str):
        """
        This method just merge an default url and http method name.
        """
        return self.url_ + method

    def get_params(self, fields: str, pdict: dict):
        """
        This method just merge http request parameters.
        """
        return {'access_token': self.token,
                'v': '5.81',
                'fields': fields} | pdict

    @staticmethod
    def transform_param(param: dict):
        return ''.join([f'&{key}={value}' for key, value in param.items()])

    def get_personal_data(self, user_id: str) -> dict | str:
        """
        Gets a user's data by user id
        :param user_id: user identification number
        :return: requests result json()
        """
        result = requests.get(self.get_url(method="users.get"),
                              params=self.transform_param(
                                  self.get_params(
                                      fields='bdate,'
                                             'sex,'
                                             'city,'
                                             'interests,'
                                             'music',
                                      pdict={'user_ids': user_id})
                              ), timeout=5)

        time.sleep(0.3)
        if result.status_code == 200 and 'response' in result.json():
            return result.json()
        else:
            pprint(result.json())
            return f"Error"

    def get_photo_f_profile(self, user_id: str, album_name: str) -> dict | str:
        """
        Gets a user's photos data by user id
        :param user_id: user identification number
        :param album_name: photos album name
        :return: requests result json()
        """
        result = requests.get(self.get_url(method="photos.get"),
                              params=self.transform_param(
                                  self.get_params(
                                      fields='',
                                      pdict={'owner_id': user_id,
                                             'album_id': album_name,
                                             'count': '200',
                                             'photo_sizes': '1',
                                             'extended': '1'})),
                              timeout=5)

        time.sleep(0.3)

        if result.status_code == 200 and 'response' in result.json():
            return result.json()['response']['items']
        else:
            pprint(result.json())
            return f"Error"

    def get_photo_f_profile_by_album_list(self, user_id: str, album_name_list: list) -> list | str:
        """
        Gets a user's photos data by user id in album_name_list
        :param user_id: user identification number
        :param album_name_list: list of photos album names
        :return: up request result:
                requests result json() or list of photos
        """
        photos_list = []
        for album_name in album_name_list:
            print(f'album_name: {album_name}')
            result = requests.get(self.get_url(method="photos.get"),
                                  params=self.transform_param(
                                      self.get_params(
                                          fields='',
                                          pdict={'owner_id': user_id,
                                                 'album_id': str(album_name),
                                                 'count': '200',
                                                 'photo_sizes': '1',
                                                 'extended': '1'})),
                                  timeout=5)
            time.sleep(0.3)
            if result.status_code == 200 and 'response' in result.json():
                photos_list.append(result.json()['response']['items'])

        return photos_list

    def search_albums(self, user_id: str) -> list:
        """
        Gets albums list.
        :param user_id: user identification number
        :return: depends of request result:
                requests result json() or list of photos album names
        """
        album_list = []
        result = requests.get(self.get_url(method="photos.getAlbums"),
                              params=self.transform_param(
                                  self.get_params(
                                      fields='',
                                      pdict={'owner_id': user_id})),
                              timeout=5)
        # pprint(result.json())
        time.sleep(0.3)

        result = result.json()
        if 'response' not in result:
            pprint(result)
        else:
            for items in result['response']['items']:
                album_list.append(items['id'])

        return album_list

    def get_thousand_users(self, city_name: str, age_min: str, age_max: str):
        """
        Gets a user's data by user id
        :param city_name
        :param age_min
        :param age_max: user identification number
        :return: requests result json()
        """
        result = requests.get(self.get_url(method="users.search"),
                              params=self.transform_param(
                                  self.get_params(
                                      fields='bdate,'
                                             'sex,'
                                             'city,'
                                             'interests,'
                                             'music',
                                      pdict={'count': '1000',
                                             'has_photo': '1',
                                             'sex': '0',
                                             'hometown': city_name,
                                             'age_from': age_min,
                                             'age_to': age_max})
                              ), timeout=5)

        time.sleep(0.3)
        if result.status_code == 200 and 'response' in result.json():
            return result.json()
        else:
            pprint(result.json())
            return f"Error"
