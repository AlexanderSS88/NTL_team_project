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
        self.vk = VkUrl('vk_token.txt')
        self.vk_ = VkUrl('vk_token_.txt')

        # get personal data
        self.pers_data_json = (self.vk.get_personal_data(user_id=self.user_id))
        # get person age
        self.age = self.get_age(self.pers_data_json['response'][0])
        # get city name
        self.sity_name = self.pers_data_json['response'][0]['city']['title']
        self.sity_id = self.pers_data_json['response'][0]['city']['id']
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

    @staticmethod
    def get_age(pers_data_json: dict):
        """
        Calculate Age from date of birth
        """
        data_ = datetime.strptime(pers_data_json['bdate'], '%d.%m.%Y')
        return datetime.now().year - data_.year

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

        for photo in photo_list[0]:
            max_photo = max(photo['sizes'], key=lambda size: int(size['width']))

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
