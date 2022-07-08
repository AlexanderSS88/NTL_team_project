from pprint import pprint
from cls.cls_Person import Person

"""
Get user data by user id.
This function is separated to use for different persons in main.
"""


def get_personal_data(user_id: int):
    user = Person(str(user_id))

    print(user)
    print()
    pprint(user.get_person_data())


if __name__ == '__main__':
    vk_id = 1
    get_personal_data(vk_id)
