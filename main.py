from pprint import pprint
from cls.cls_Person import Person
from cls.cls_DataBaseExchange import DataBaseExchange
from vk_tools.cls_application import Application

"""
Get user data by user id.
This function is separated to use for different persons in main.
"""

data_base = DataBaseExchange()


def get_personal_data(user_id: str):
    user = Person(str(user_id))
    print()

    if user.data_are_good:
        # print('Version for Bot:')
        # print(user)
        user_dict = user.get_person_data()
        print('Version for Database:')
        pprint(user_dict)
        data_base.add_user_data(user_dict)

        # user.get_photos_of_person(user.user_id)
        # data_base.add_user_photos(user_dict, user.photo_list, user.photo_id_list)
        # data_base.add_user_interests(user_dict)

        print('Data from VK:')
        photos_list_, photos_id_list_ = get_photo_list(user_id)
        print(photos_list_)
        print(photos_id_list_)
        data_base.add_user_photos(user_dict, user.photo_list, user.photo_id_list)
        data_base.add_user_interests(user_dict)

        # get_personal_data(3)
        #
        # print('Data 2 from VK:')
        # photos_list_, photos_id_list_ = get_photo_list(user_id)
        # data_base.add_user_photos(user_dict, photos_list_, photos_id_list_)


    else:
        print('The person data are not useful.')

def get_photo_list(user_id):
    user = Person(user_id)
    # print('Data from DB:')
    # photos_id_list, photos_list = data_base.get_photo_from_db(user_id)
    # print(photos_list)
    # print(photos_id_list)

    print('Data from VK:')
    photos_list = user.get_photos_of_person(user_id)
    photos_id_list = user.photo_id_list
    print(photos_list)
    print(photos_id_list)


    return photos_list, photos_id_list


def bot_cycle():
    bot = Application()

    while True:
        dialog = bot.new_companion()

        # если клиент не против, можно начть новый цикл опроса
        if 'Have dialog.' in dialog:
            pers_list = bot.get_data_4_candidates_list()
            print(f'pers_list: {pers_list}')
            if 'Fail' in pers_list:
                bot.write_msg('Может в следующий раз?')
                break
            if (len(pers_list)) == 0:
                bot.write_msg(
                    'Извини, никого не нашлось:(\nМожет в следующий раз?\nСпасибо что воспользовались нашим сервисом.')
                break

            bot.write_msg('Теперь посмотрим кого удалось отыскать.\n')
            bot_person = bot.person_list_presentation(pers_list)
            if bot_person == 'Complete':
                bot.write_msg('Это были все кандидаты.\nСпасибо что воспользовались нашим сервисом.')
                # break
            elif bot_person == 'Canceled':
                bot.write_msg('Может в следующий раз?\nСпасибо что воспользовались нашим сервисом.')
                # break
            elif bot_person == 'Stop':
                return 'Canceled by User'

        # выход из программы
        if 'Stop' in dialog:
            return 'Canceled by User'


if __name__ == '__main__':

    data_base.create_tables()

    while True:
        command = input("Please choose the command: \n"
                        "'s'-scan VKontakte users to add to DataBase,\n"
                        "'c' -get candidates list, \n"
                        "'p' -get photos list, \n"
                        "'b' -start bot, \n"
                        "'q'- to quit: \t")
        match command:
            case 'q':
                break
            case 's':
                start_id = input("Input start user id for scan:\t")
                last_id = input("Input last user id for scan:\t")
                for vk_id in range(int(start_id), int(last_id)):
                    print(f'vk_id: {vk_id}')
                    get_personal_data(vk_id)
            case 'c':
                min_ege = input("Input min age of candidate:\t")
                max_age = input("Input max age of candidate:\t")
                city = input("Input the city name:\t")
                candidates_list = data_base.get_candidates(min_age=int(min_ege),
                                                           max_age=int(max_age),
                                                           city_name=city)
                print(candidates_list)
            case 'p':
                user_id_4_photo = input("Input user id:\t")
                get_photo_list(user_id_4_photo)
                # user = Person(user_id_4_photo)
                # print('Data from VK:')
                # photos_list = user.get_photos_of_person(user_id_4_photo)
                # photos_id_list = user.photo_id_list
                # print(photos_list)
                # print(photos_id_list)
                # print('Data from DB:')
                # photos_id_list, photos_list = data_base.get_photo_from_db(user_id_4_photo)
                # print('From DB:')
                # print(photos_list)
                # print(photos_id_list)
            case 'b':
                print(bot_cycle())
