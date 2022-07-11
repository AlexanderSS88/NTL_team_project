import requests
import time
from cls.cls_HttpReq import HttpR

# from pprint import pprint

"""
This is the VKontakte API communication class
"""


class VkUrl(HttpR):
    url_ = "https://api.vk.com/method/"

    def __init__(self, token_file_n: str):
        super().__init__(token_file_n)

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

    def get_base_personal_data(self, user_id: str) -> dict:
        """
        Gets a user's data by user id
        """
        result = requests.get(self.get_url(method="users.get"),
                              params=self.transform_param(
                                  self.get_params(
                                      fields='bdate,'
                                             'sex,'
                                             'city,'
                                      # 'photo_400_orig,'
                                             'interests,'
                                             'music',
                                      pdict={'user_ids': user_id})
                              ), timeout=5)

        time.sleep(0.3)
        return result.json()

    def get_personal_data(self, user_id: str) -> dict:
        """
        Gets a user's data by user id
        """
        result = requests.get(self.get_url(method="users.get"),
                              params=self.transform_param(
                                  self.get_params(
                                      fields='bdate,'
                                             'sex,'
                                             'city,'
                                      # 'photo_400_orig,'
                                             'interests,'
                                             'music',
                                      pdict={'user_ids': user_id})
                              ), timeout=5)

        time.sleep(0.03)
        return result.json()

    def get_photo_f_profile(self, user_id: str, album_name: str) -> dict | str:

        """
        Gets a user's photos data by user id
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

        if result.status_code == 200 and 'error' not in result.json():
            return result.json()['response']['items']
        else:
            return f"Error"

    def get_photo_f_profile_by_album_list(self, user_id: str, album_name_list: list) -> list | str:

        """
        Gets a user's photos data by user id in album_name_list
        """

        photos_list = []

        for album_name in album_name_list:
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

            if result.status_code != 200 or 'error' in result.json():
                return f"Error"
            else:
                photos_list.append(result.json()['response']['items'])

        return photos_list

    def search_albums(self, user_id: str) -> list:
        """
        Gets albums list.
        """

        album_list = []
        result = requests.get(self.get_url(method="photos.getAlbums"),
                              params=self.transform_param(
                                  self.get_params(
                                      fields='',
                                      pdict={'owner_id': user_id})),
                              timeout=5)
        time.sleep(0.3)

        result = result.json()

        for items in result['response']['items']:
            album_list.append(items['id'])

        return album_list
