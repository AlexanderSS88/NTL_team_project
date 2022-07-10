from pprint import pprint
from cls.cls_Person import Person
from cls.cls_DataBaseExchange import DataBaseExchange

"""
Get user data by user id.
This function is separated to use for different persons in main.
"""


def get_personal_data(user_id: int):
    user = Person(str(user_id))
    # user.get_photos_of_person()

    print('Version for Bot:')
    print(user)
    print()
    print('Version for Database')
    pprint(user.get_person_data())

    data_base = DataBaseExchange()
    data_base.add_user_data(user.get_person_data())


if __name__ == '__main__':

    for vk_id in range(84482600, 84482670):
        print(f'vk_id: {vk_id}')
        get_personal_data(vk_id)
