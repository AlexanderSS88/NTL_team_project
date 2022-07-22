from cls.cls_DataBaseExchange import DataBaseExchange
from cls.cls_json import Add2Json


def bot_cycle(self, from_json=False):
    """
    This is the base VK bot cycle.
    :param from_json: use json storage file of not
    """
    clients_dict = {}

    while True:
        new_id, message, event_type = self.get_external_call()

        if new_id not in clients_dict.keys():
            self.wellcome(new_id, message)
            clients_dict.setdefault(new_id)  # добавляем клиента в словарь
            clients_dict[new_id] = {'dialog_status': 'wellcome'}  # спросили, хочешь знакомиться
        else:
            match clients_dict[new_id]['dialog_status']:
                case 'wellcome':
                    opinion = self.get_user_opinion(new_id, message)  # ответ на "хочешь знакомиться"
                    match opinion:
                        case 'No':
                            self.write_msg(user_id=new_id,
                                           message="Как знаешь.\nЕсли что, я тут, обращайся")
                            clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                        case 'Yes':
                            self.ask_user_yes_no(user_id=new_id,
                                                 message="Теперь мне потребуются некоторые входные данные:\n"
                                                         " - возрастной интервал кандидатов "
                                                         "(минимальный и максимальный возраст);\n"
                                                         " - город их проживания.\n"
                                                         "Продолжим?")

                            clients_dict[new_id]['dialog_status'] = 'question#1'

                case 'question#1':
                    opinion = self.get_user_opinion(new_id, message)  # Продолжим?"
                    match opinion:
                        case 'No':
                            self.write_msg(user_id=new_id,
                                           message="Как знаешь.\nЕсли что, я тут, обращайся")
                            clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                        case 'Yes':
                            self.write_msg(user_id=new_id,
                                           message="Тогда приступим!\n"
                                                   "Напиши минимальный возраст кандидата:")
                            clients_dict[new_id]['dialog_status'] = 'question#2'
                case 'question#2':
                    min_age = message
                    if self.is_age_valid(min_age):
                        clients_dict[new_id].setdefault('candidates_data')
                        clients_dict[new_id]['candidates_data'] = {'min_age': min_age}
                        clients_dict[new_id]['dialog_status'] = 'question#3'
                        self.write_msg(user_id=new_id,
                                       message="Напиши максимальный возраст кандидата:")
                    else:
                        self.write_msg(user_id=new_id,
                                       message="Извини, с возрастом что-то не так...")
                case 'question#3':
                    max_age = message
                    if self.is_age_valid(max_age):
                        clients_dict[new_id]['candidates_data'].setdefault('max_age', max_age)

                        # проверяем, если возраст перепутан
                        if int(clients_dict[new_id]['candidates_data']['min_age']) > \
                                int(clients_dict[new_id]['candidates_data']['max_age']):
                            clients_dict[new_id]['candidates_data']['min_age'], \
                            clients_dict[new_id]['candidates_data']['max_age'] = \
                                clients_dict[new_id]['candidates_data']['max_age'], \
                                clients_dict[new_id]['candidates_data']['min_age']

                        clients_dict[new_id]['dialog_status'] = 'question#4'
                        self.write_msg(user_id=new_id,
                                       message="Напиши город, где живёт кандидат:")
                    else:
                        self.write_msg(user_id=new_id,
                                       message="Извини, с возрастом что-то не так...")
                case 'question#4':
                    clients_dict[new_id]['candidates_data'].setdefault('city', message)
                    self.write_msg(user_id=new_id,
                                   message="Теперь посмотрим кого удалось отыскать.")

                    if from_json:
                        print("Get data from json.")
                        add_jeson = Add2Json('db_in_json.json')

                        candidates_list = add_jeson.get_candidates_from_json(
                            min_age=int(clients_dict[new_id]['candidates_data']['min_age']),
                            max_age=int(clients_dict[new_id]['candidates_data']['max_age']),
                            city_name=clients_dict[new_id]['candidates_data']['city'])
                    else:
                        print("Get data from DataBase.")
                        data_base = DataBaseExchange()

                        candidates_list = data_base.get_candidates(
                            min_age=int(clients_dict[new_id]['candidates_data']['min_age']),
                            max_age=int(clients_dict[new_id]['candidates_data']['max_age']),
                            city_name=clients_dict[new_id]['candidates_data']['city'])
                    # Если никого не нашлось
                    if len(candidates_list) == 0:
                        self.write_msg(user_id=new_id,
                                       message='Извини, никого не нашлось:(\nМожет в следующий раз?'
                                               '\nСпасибо что воспользовались нашим сервисом.')
                        clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                    else:
                        # собираем список кандидатов
                        clients_dict[new_id].setdefault('candidates_list', candidates_list)
                        clients_dict[new_id].setdefault('favorite_list', [])

                        # по типу стека достаём последнего кандидата
                        candidate_id = clients_dict[new_id]['candidates_list'].pop() # удаляем этого кандидата из стека
                        # создаём переменную текущего кандидата, вдруг он попадёт в избранное!
                        clients_dict[new_id].setdefault('current_candidate', candidate_id)

                        # clients_dict[new_id]['candidates_list'].pop()

                        if from_json:
                            print("Get data from json.")
                            self.person_presentation_f_json(new_id, candidate_id)
                        else:
                            print("Get data from DataBase.")
                            self.person_presentation(new_id, candidate_id)

                        # спрашиваем мнение пользователя об кандидате:
                        # в избранное,
                        # посомтреть избранное,
                        # следующий,
                        # закончить
                        self.ask_user_about_candidate(user_id=new_id,
                                                      message='Что скажешь?')

                        clients_dict[new_id]['dialog_status'] = 'presentation'

                case 'presentation':
                    if event_type == 'text': # Продолжим?"
                        message = self.check_user_opinion_in_presentation(message, new_id)
                    # смотрим что ответил пользователь
                    match message:
                        case 'add_to_favor': # добавить в избранное
                            clients_dict[new_id]['favorite_list'].append(clients_dict[new_id]['current_candidate'])
                        case 'complete': # завершить
                            if not clients_dict[new_id]['favorite_list']:
                                self.write_msg(user_id=new_id,
                                               message="Как знаешь.\nЕсли что, я тут, обращайся")
                            else:
                                # выводим список избранных
                                self.write_msg(user_id=new_id,
                                               message="Давай посмотрим, кого ты выбрал:")
                                for favorite in clients_dict[new_id]['favorite_list']:
                                    # для каждого идентификатора избранного получаем данные
                                    if from_json:
                                        print("Get data from json.")
                                        self.person_presentation_f_json(new_id, favorite)
                                    else:
                                        print("Get data from DataBase.")
                                        self.person_presentation(new_id, favorite)

                            clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                        case 'open_favor': # выводим избранных
                            self.write_msg(user_id=new_id,
                                           message="Давай посмотрим, кого ты выбрал:")
                            for favorite in clients_dict[new_id]['favorite_list']:
                                # для каждого идентификатора избранного получаем данные
                                if from_json:
                                    print("Get data from json.")
                                    self.person_presentation_f_json(new_id, favorite)
                                else:
                                    print("Get data from DataBase.")
                                    self.person_presentation(new_id, favorite)
                            self.ask_user_after_favor(user_id=new_id,
                                                      message='Продолжим?')

                        case 'next':
                            self.delete_messages(new_id)

                            #  Если список иссяк
                            if not clients_dict[new_id]['candidates_list']:
                                if not clients_dict[new_id]['favorite_list']:
                                    self.write_msg(user_id=new_id,
                                                   message='Извини, больше никого не нашлось:(\n'
                                                           'Может в следующий раз?\n'
                                                           'Спасибо что воспользовались нашим сервисом.')
                                else:
                                    self.write_msg(user_id=new_id,
                                                   message="Давай посмотрим, кого ты выбрал:")
                                    for favorite in clients_dict[new_id]['favorite_list']:
                                        if from_json:
                                            print("Get data from json.")
                                            self.person_presentation_f_json(new_id, favorite)
                                        else:
                                            print("Get data from DataBase.")
                                            self.person_presentation(new_id, favorite)
                                self.write_msg(user_id=new_id,
                                               message='Спасибо что воспользовались нашим сервисом.')
                                clients_dict.pop(new_id)  # удалили клиента из списка, разговор окончен
                            else:
                                candidate_id = clients_dict[new_id]['candidates_list'].pop()
                                clients_dict[new_id]['current_candidate'] = candidate_id

                                # bot.person_presentation(new_id, candidate_id)
                                if from_json:
                                    print("Get data from json.")
                                    self.person_presentation_f_json(new_id, candidate_id)
                                else:
                                    print("Get data from DataBase.")
                                    self.person_presentation(new_id, candidate_id)

                                clients_dict[new_id]['dialog_status'] = 'presentation'
                                self.ask_user_about_candidate(user_id=new_id,
                                                              message='Что скажешь?')
