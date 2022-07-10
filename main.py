from pprint import pprint
from cls.cls_Person import Person
from cls.cls_DataBaseExchange import DataBaseExchange

"""
Get user data by user id.
This function is separated to use for different persons in main.
"""


def get_personal_data(user_id: int):
    user = Person(str(user_id))
    user.get_photos_of_person()

    print('Version for Bot:')
    print(user)
    print()
    print('Version for Database')
    pprint(user.get_person_data())


if __name__ == '__main__':
    data_base = DataBaseExchange()

    # vk_id = 668524
    # get_personal_data(vk_id)
