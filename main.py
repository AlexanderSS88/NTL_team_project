from pprint import pprint
import time
from cls.cls_Person import Person
from cls.cls_DataBaseExchange import DataBaseExchange
from vk_tools.cls_application import Application
from cls.cls_json import Add2Json

"""
Get user data by user id.
This function is separated to use for different persons in main.
"""


def get_personal_data(user_id: str, write_2_json: str):
    user = Person(str(user_id))
    print()

    data_base = DataBaseExchange()

    if user.data_are_good:
        user_dict = user.get_person_data()
        print('Version for Database:')
        pprint(user_dict)
        data_base.add_user_data(user_dict)

        print('Data from VK:')
        photos_list, photos_id_list = get_photo_list_from_VK(user_id)
        print(f'photos_list_: {photos_list}')
        print(f'photos_id_list_: {photos_id_list}')
        data_base.add_user_photos(user_dict, photos_list, photos_id_list)
        # data_base.add_user_interests(user_dict)

        if write_2_json == 'y':
            user_dict.setdefault('photos_id_list', photos_id_list)
            print('\nVersion for json:')
            pprint(user_dict)
            print()

            add_jeson = Add2Json('db_in_json.json')
            add_jeson.add_2_json(user_id, user_dict)
        else:
            print('User data saved in DataBase only.')

    else:
        print('The person data are not useful.')


def get_photo_list_from_VK(user_id):
    user = Person(user_id)

    print('Data from VK:')
    photos_list = user.get_photos_of_person(user_id)
    photos_id_list = user.photo_id_list
    print(photos_list)
    print(photos_id_list)

    return photos_list, photos_id_list


def get_photo_list_from_DB(user_id):
    data_base = DataBaseExchange()
    print('Data from DB:')
    photos_id_list, photos_list = data_base.get_photo_from_db(user_id)
    print(photos_list)
    print(photos_id_list)

    return photos_list, photos_id_list


def bot_cycle():
    bot = Application()
    clients_dict = {}

    while True:
        new_id, message = bot.get_external_call()

        if new_id not in clients_dict.keys():
            bot.wellcome(new_id, message)
            clients_dict.setdefault(new_id)  # добавляем клиента в словарь
            clients_dict[new_id] = {'dialog_status': 'wellcome'}  # спросили, хочешь знакомиться
        else:
            match clients_dict[new_id]['dialog_status']:
                case 'wellcome':
                    opinion = bot.get_user_opinion(new_id, message)  # ответ на "хочешь знакомиться"
                    match opinion:
                        case 'No':
                            bot.write_msg(user_id=new_id,
                                          message="Как знаешь.\nЕсли что, я тут, обращайся")
                            clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                        case 'Yes':
                            bot.write_msg(user_id=new_id,
                                          message="Теперь мне потребуются некоторые входные данные:\n"
                                                  " - возрастной интервал кандидатов "
                                                  "(минимальный и максимальный возраст);\n"
                                                  " - город их проживания.\n"
                                                  "Продолжим?")

                            clients_dict[new_id]['dialog_status'] = 'question#1'

                case 'question#1':
                    opinion = bot.get_user_opinion(new_id, message)  # Продолжим?"
                    match opinion:
                        case 'No':
                            bot.write_msg(user_id=new_id,
                                          message="Как знаешь.\nЕсли что, я тут, обращайся")
                            clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                        case 'Yes':
                            bot.write_msg(user_id=new_id,
                                          message="Тогда приступим!\n"
                                                  "Напиши минимальный возраст кандидата:")
                            clients_dict[new_id]['dialog_status'] = 'question#2'
                case 'question#2':
                    min_age = message
                    if bot.is_age_valid(min_age):
                        clients_dict[new_id].setdefault('candidates_data')
                        clients_dict[new_id]['candidates_data'] = {'min_age': min_age}
                        clients_dict[new_id]['dialog_status'] = 'question#3'
                        bot.write_msg(user_id=new_id,
                                      message="Напиши максимальный возраст кандидата:")
                    else:
                        bot.write_msg(user_id=new_id,
                                      message="Извини, с возрастом что-то не так...")
                case 'question#3':
                    max_age = message
                    if bot.is_age_valid(max_age):
                        clients_dict[new_id]['candidates_data'].setdefault('max_age', max_age)

                        # проверяем, если возраст перепутан
                        if int(clients_dict[new_id]['candidates_data']['min_age']) > \
                                int(clients_dict[new_id]['candidates_data']['max_age']):
                            clients_dict[new_id]['candidates_data']['min_age'], \
                            clients_dict[new_id]['candidates_data']['max_age'] = \
                                clients_dict[new_id]['candidates_data']['max_age'], \
                                clients_dict[new_id]['candidates_data']['min_age']

                        clients_dict[new_id]['dialog_status'] = 'question#4'
                        bot.write_msg(user_id=new_id,
                                      message="Напиши город, где живёт кандидат:")
                    else:
                        bot.write_msg(user_id=new_id,
                                      message="Извини, с возрастом что-то не так...")
                case 'question#4':
                    clients_dict[new_id]['candidates_data'].setdefault('city', message)
                    bot.write_msg(user_id=new_id,
                                  message="Теперь посмотрим кого удалось отыскать.")

                    data_base = DataBaseExchange()

                    candidates_list = data_base.get_candidates(
                        min_age=int(clients_dict[new_id]['candidates_data']['min_age']),
                        max_age=int(clients_dict[new_id]['candidates_data']['max_age']),
                        city_name=clients_dict[new_id]['candidates_data']['city'])

                    if candidates_list == 0:
                        bot.write_msg(user_id=new_id,
                                      message='Извини, никого не нашлось:(\nМожет в следующий раз?'
                                              '\nСпасибо что воспользовались нашим сервисом.')
                        clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                    else:
                        clients_dict[new_id].setdefault('candidates_list', candidates_list)

                        candidate_id = clients_dict[new_id]['candidates_list'][-1]
                        clients_dict[new_id]['candidates_list'].pop()

                        bot.person_presentation(new_id, candidate_id)

                        clients_dict[new_id]['dialog_status'] = 'presentation'
                        bot.write_msg(user_id=new_id, message='Следующий?')
                case 'presentation':
                    opinion = bot.get_user_opinion(new_id, message)  # Продолжим?"
                    match opinion:
                        case 'No':
                            bot.write_msg(user_id=new_id,
                                          message="Как знаешь.\nЕсли что, я тут, обращайся")
                            clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                        case 'Yes':
                            if clients_dict[new_id]['candidates_list'] == []:
                                bot.write_msg(user_id=new_id,
                                              message='Извини, больше никого не нашлось:(\n'
                                                      'Может в следующий раз?\n'
                                                      'Спасибо что воспользовались нашим сервисом.')
                                clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                            else:
                                candidate_id = clients_dict[new_id]['candidates_list'][-1]
                                clients_dict[new_id]['candidates_list'].pop()

                                bot.person_presentation(new_id, candidate_id)

                                clients_dict[new_id]['dialog_status'] = 'presentation'
                                bot.write_msg(user_id=new_id, message='Следующий?')


if __name__ == '__main__':

    data_base = DataBaseExchange()
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
                write_2_json = input("Should program write data to json file? (y/n):\t")

                for vk_id in range(int(start_id), int(last_id)):
                    print(f'vk_id: {vk_id}')
                    get_personal_data(vk_id, write_2_json)
                    time.sleep(0.7)
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
                get_photo_list_from_DB(user_id_4_photo)
            case 'b':
                print(bot_cycle())
