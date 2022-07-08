from pprint import pprint
from datetime import datetime
from cls.cls_VkUrl import VkUrl

"""
Class to describe user person.
"""


class Person:
    def __init__(self, user_id):
        self.user_id = user_id
        self.photo_quantity = 3

        # tokens for different access kind
        self.vk = VkUrl('tokens/vk_token.txt')
        self.vk_ = VkUrl('tokens/vk_bot.txt')

        # get personal data
        self.pers_data_json = (self.vk.get_personal_data(user_id=self.user_id))
        # pprint(self.pers_data_json)
        # get person age
        self.age = self.get_age(self.pers_data_json['response'][0])
        # get city name
        self.sity_name = self.pers_data_json['response'][0]['city']['title']
        self.sity_id = self.pers_data_json['response'][0]['city']['id']
        self.interests = self.get_interests(self.pers_data_json['response'][0]['interests'])
        # the base albums list, common for everybody
        self.album_list = ['wall', 'profile']
        # search another albums
        self.album_list.extend(self.vk_.search_albums(user_id=user_id))
        # get a list of all photos from all albums
        self.photo_list = self.vk.get_photo_f_profile_by_album_list(user_id=self.user_id,
                                                                    album_name_list=self.album_list)
        # sort of photos by bigger likes quantity and take 3 best
        self.photo_list = self.format_files_list(self.photo_list, self.photo_quantity)

    def __str__(self):
        """
        :return: the person information for bot
        """
        n_char = '\n'
        return f"{self.pers_data_json['response'][0]['first_name']} {self.pers_data_json['response'][0]['last_name']}" \
               f"\nhttps://vk.com/id{self.user_id}\nattachment({''.join([f'{url},{n_char}' for url in self.photo_list])})"

    def get_person_data(self):
        """
        :return: the person information in short dictionary
        """
        return {'first_name': self.pers_data_json['response'][0]['first_name'],
                'last_name': self.pers_data_json['response'][0]['last_name'],
                'age': self.age,
                'city': self.sity_name,
                'city_id': self.sity_id,
                'interests': self.interests,
                'photos_list': self.photo_list}

    @staticmethod
    def get_age(pers_data_json: dict):
        """
        Calculate Age from date of birth
        """
        data_str = pers_data_json.get('bdate')
        if data_str is not None:
            data_ = datetime.strptime(data_str, '%d.%m.%Y')
            return datetime.now().year - data_.year
        else:
            return None

    @staticmethod
    def get_interests(intr_str: str) -> list:
        interests = []
        if len(intr_str) >0:
            interests = intr_str.split('.')
        return interests


    @staticmethod
    def format_files_list(photo_list: dict, qtt: int) -> list:
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

        for item in photo_list:
            for photo in item:
                # max_photo = max(photo['sizes'], key=lambda size: int(size['width']))
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
