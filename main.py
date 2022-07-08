from pprint import pprint

from cls.cls_VkUrl import VkUrl
from cls.cls_Person import Person

"""
Get user data by user id.
This function is separated to use for different persons in main.
"""


def get_personal_data(user_id: int):
    user = Person(str(user_id))

    print(user)


if __name__ == '__main__':
    vk_id = 84482680
    get_personal_data(vk_id)
