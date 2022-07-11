from pprint import pprint
from datetime import datetime
from cls.cls_VkUrl import VkUrl

import pathlib
from pathlib import Path

"""
Class to describe user person.
"""


class Person:
    # the base albums list, common for everybody
    album_list = ['wall', 'profile']
    photo_list = []
    city_name = str
    city_id = str

    def __init__(self, user_id):
        self.user_id = user_id
        self.photo_quantity = 3

        # marker of good user data
        self.data_are_good = True

        # tokens for different access kind
        path = Path(pathlib.Path.cwd(), 'tokens', 'vk_bot.txt')
        self.vk = VkUrl(str(path))
        path = Path(pathlib.Path.cwd(), 'tokens', 'vk_bot.txt')
        self.vk_ = VkUrl(str(path))

        # get personal data
        self.pers_data_json = (self.vk.get_personal_data(user_id=self.user_id))
        # pprint(self.pers_data_json)
        self.successful_read = True

        if self.test_response(self.pers_data_json):
            personal_dict = self.pers_data_json['response'][0]
            # get person age
            self.age = self.get_age(personal_dict)
            self.sex = personal_dict.get('sex')
            # get city name
            self.get_city(personal_dict)

            self.interests = self.get_interests(personal_dict)
        else:
            self.data_are_good = False
            print('Error')
            self.successful_read = False

    def __str__(self):
        """
        :return: the person information for bot
        """
        n_char = '\n'

        if self.successful_read:
            return f"{self.pers_data_json['response'][0]['first_name']} " \
                   f"{self.pers_data_json['response'][0]['last_name']}" \
                   f"\nhttps://vk.com/id{self.user_id}\n" \
                   f"attachment({''.join([f'{url},{n_char}' for url in self.photo_list])})"
        else:
            return 'Error'

    def get_photos_of_person(self) -> list:

        # search another albums
        self.album_list.extend(self.vk_.search_albums(user_id=self.user_id))
        # get a list of all photos from all albums
        self.photo_list = self.vk.get_photo_f_profile_by_album_list(user_id=self.user_id,
                                                                    album_name_list=self.album_list)
        # sort of photos by bigger likes quantity and take 3 best
        self.photo_list = self.format_files_list(self.photo_list, self.photo_quantity)

        return self.photo_list

    def get_photos_of_person(self, user_id) -> list:

        # search another albums
        self.album_list.extend(self.vk_.search_albums(user_id=user_id))
        # get a list of all photos from all albums
        self.photo_list = self.vk.get_photo_f_profile_by_album_list(user_id=user_id,
                                                                    album_name_list=self.album_list)
        # sort of photos by bigger likes quantity and take 3 best
        self.photo_list = self.format_files_list(self.photo_list, self.photo_quantity)

        return self.photo_list

    def get_city(self, pers_data_json: dict):
        city_dict = pers_data_json.get('city')
        if city_dict is None:
            self.city_name = 'Unknown'
            self.city_id = -1
            self.data_are_good = False
            return

        self.city_name = city_dict.get('title')
        if self.city_name is None:
            self.data_are_good = False
            self.city_name = 'Unknown'

        self.city_id = city_dict.get('id')
        if self.city_id is None:
            self.city_id = -1

    @staticmethod
    def test_response(response: dict) -> bool:
        return 'response' in response

    def get_person_data(self):
        """
        :return: the person information in short dictionary
        """
        if self.successful_read:
            return {'first_name': self.pers_data_json['response'][0]['first_name'],
                    'last_name': self.pers_data_json['response'][0]['last_name'],
                    'id': self.user_id,
                    'url': f'https://vk.com/id{self.user_id}',
                    'age': self.age,
                    'sex': self.sex,
                    'city': self.city_name,
                    'city_id': self.city_id,
                    'interests': self.interests,
                    'photos_list': self.photo_list}
        else:
            return 'Error'

    def get_age(self, pers_data_json: dict):
        """
        Calculate Age from date of birth
        """
        data_str = pers_data_json.get('bdate')
        if data_str is not None:
            try:
                data_ = datetime.strptime(data_str, '%d.%m.%Y')
            except ValueError:
                self.data_are_good = False
                return -1

            return datetime.now().year - data_.year
        else:
            self.data_are_good = False
            return -1

    @staticmethod
    def get_interests(pers_data_json: dict) -> list:
        data_str = pers_data_json.get('interests')
        interests = []
        if data_str is not None:
            if len(data_str) > 0:
                interests = data_str.split('.')
        return interests

    @staticmethod
    def format_files_list(photo_list: list, qtt: int) -> list:
        """
        Format a list of files_inf_list by template:
            [{
            "file_name": "34.jpg",
            "likes": "likes"
            "data": "data"
            "url": url to download
            "size": "z"
            "width": width of photo
            }]
        :return: list of urls
        """
        files_inf_list = list()

        if 'Error' in photo_list:
            return files_inf_list

        for item in photo_list:
            for photo in item:
                max_photo = photo['sizes'][-1]

                file_name = f"{photo['likes']['count']}.jpeg"

                # Collect the list of files.
                files_inf_list.append({'file_name': file_name,
                                       'likes': photo['likes']['count'],
                                       'date': photo['date'],
                                       'url': max_photo['url'],
                                       'size': max_photo['type'],
                                       'width': max_photo['width']})

        files_inf_list.sort(key=lambda x: int(x['likes']), reverse=True)

        if len(files_inf_list) < qtt:
            qtt = len(files_inf_list)

        files_inf_list = [files_inf_list[i]['url'] for i in range(qtt)]

        return files_inf_list
