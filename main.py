import time
from pprint import pprint
from cls.cls_DataBaseExchange import DataBaseExchange
from vk_tools.cls_application import Application

if __name__ == '__main__':

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
                data_base = DataBaseExchange()
                bot = Application()
                data_base.create_tables()
                start_id = input("Input start user id for scan:\t")
                last_id = input("Input last user id for scan:\t")
                write_2_json = input("Should program write data to json file? (y/n):\t")
                for vk_id in range(int(start_id), int(last_id)):
                    bot.get_personal_data(str(vk_id), write_2_json)
                    time.sleep(0.7)
            case 'c':
                data_base = DataBaseExchange()
                min_ege = input("Input min age of candidate:\t")
                max_age = input("Input max age of candidate:\t")
                city = input("Input the city name:\t")
                candidates_list = data_base.get_candidates(min_age=int(min_ege),
                                                           max_age=int(max_age),
                                                           city_name=city)
                print(candidates_list)
            case 'p':
                bot = Application()
                user_id_4_photo = input("Input user id:\t")
                photos_list, photos_id_list = bot.get_photo_list_from_db(user_id_4_photo)
                print(f'photos_id_list: {photos_id_list}')
                print('photos_list:')
                pprint(photos_list)
            case 'b':
                bot = Application()
                data_source = input("Take data from DataBase (any key) "
                                    "or from json file (j)?:\t")
                if data_source == 'j':
                    print(bot.bot_cycle(from_json=True))
                else:
                    print(bot.bot_cycle())
