from pprint import pprint
from cls.cls_Person import Person
from cls.cls_DataBaseExchange import DataBaseExchange

"""
Get user data by user id.
This function is separated to use for different persons in main.
"""

data_base = DataBaseExchange()


def get_personal_data(user_id: int):
    user = Person(str(user_id))
    print()

    if user.data_are_good:
        # print('Version for Bot:')
        # print(user)
        user_dict = user.get_person_data()
        print('Version for Database:')
        pprint(user_dict)
        data_base.add_user_data(user_dict)
        user.get_photos_of_person(user_id)

    else:
        print('The person data are not useful.')


if __name__ == '__main__':

    data_base.create_tables()

    for vk_id in range(1, 84482670):
        print(f'vk_id: {vk_id}')
        get_personal_data(vk_id)
