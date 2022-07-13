import re
from vk_api import VkApi
from random import randrange
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from cls.cls_person_list_iteration import PersonListStack

from pprint import pprint
import pathlib
from pathlib import Path
import configparser

from cls.cls_Person import Person
from cls.cls_DataBaseExchange import DataBaseExchange


class Application:
    user_id = ()

    GROUP_ID = ()
    GROUP_TOKEN = ()
    API_VERSION = ()
    APP_ID = ()
    APPLICATION_TOKEN = ()
    OWNER_ID = ()
    CALLBACK_TYPES = ['show_snackbar', 'open_link', 'open_app']

    pattern_hi = "(прив)|(хай)|(здаров)|(салам)|(здравст)|(добр..)|(салют)|(ку)|(hi)|(ghbd)|(\[fq)"
    pattern_no = "(не)|(нет)|(нехочу)|(не хочу)|(no)|(ne)|(not)"
    pattern_yes = "(давай)|(да)|(ок)|(хорош)|(соглас)|(добро)|(ладно)|(yes)|(lf)|(yep)|(замётано)"

    def __init__(self, db_data_file_path='/tokens/application_data.ini'):
        self.take_application_data(db_data_file_path)

        if len(self.GROUP_ID) == 0:
            print(f'Error read {db_data_file_path}')
        else:
            self.vk_session = VkApi(token=self.GROUP_TOKEN, api_version=self.API_VERSION)
            self.vk = self.vk_session.get_api()

            # To use Long Poll API
            self.longpoll = VkBotLongPoll(self.vk_session, group_id=self.GROUP_ID)

    def take_application_data(self, db_data_file_path):
        path = str(Path(pathlib.Path.cwd())) + db_data_file_path

        print(path)

        config = configparser.ConfigParser()
        config.read(path)

        self.GROUP_ID = config['DEFAULT']['GROUP_ID']
        self.GROUP_TOKEN = config['DEFAULT']['GROUP_TOKEN']
        self.API_VERSION = config['DEFAULT']['API_VERSION']
        self.APPLICATION_TOKEN = config['DEFAULT']['APPLICATION_TOKEN']
        self.OWNER_ID = config['DEFAULT']['OWNER_ID']

    # Send messages
    def write_msg(self, message, user_id='default'):
        if user_id == 'default':
            user_id = self.user_id
        self.vk_session.method('messages.send',
                               {'user_id': int(user_id), 'message': message, 'random_id': randrange(10 ** 7)})

    # Цикл работы с новым пользователем
    def new_companion(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                pprint(event.object.message)

                companion_user = Person(event.object.message['from_id'])

                if event.obj.message['text'] == 'изыди':
                    self.write_msg(user_id=companion_user.user_id, message="Как скажете.")
                    return [companion_user.user_id, "Canceled by user."]
                elif re.findall(self.pattern_hi, event.obj.message['text'], flags=re.IGNORECASE):
                    message_good = f"Здаров, коль не шутишь! {companion_user.first_name}, предлагаю тебе попробовать познакомиться с кем-нибудь. Согласен? :)"
                    self.write_msg(user_id=companion_user.user_id, message=message_good)
                    for event2 in self.longpoll.listen():
                        if event2.type == VkBotEventType.MESSAGE_NEW:
                            pprint(event2.object.message)
                            if event2.obj.message['text'] == 'изыди':
                                self.write_msg(user_id=companion_user.user_id, message="Как скажете.")
                                return [companion_user.user_id, "Canceled by user."]
                            if re.findall(self.pattern_no, event2.obj.message['text'], flags=re.IGNORECASE):
                                message_no = "Как знаешь.\nЕсли что, я тут, обращайся"
                                self.write_msg(user_id=companion_user.user_id, message=message_no)
                            if re.findall(self.pattern_yes, event2.obj.message['text'], flags=re.IGNORECASE):
                                self.write_msg(user_id=companion_user.user_id, message="Тогда проиступим!")
                                self.user_id = companion_user.user_id
                                return [companion_user.user_id, "Have dialog."]

                else:
                    message_bad = f"Не здороваюсь.... {companion_user.last_name}, будешь знакомиться с кем-нибудь?"
                    self.write_msg(user_id=companion_user.user_id, message=message_bad)

                    for event2 in self.longpoll.listen():
                        if event2.type == VkBotEventType.MESSAGE_NEW:
                            pprint(event2.object.message)
                            if event2.obj.message['text'] == 'изыди':
                                self.write_msg(user_id=companion_user.user_id, message="Как скажете.")
                                return [companion_user.user_id, "Canceled by user."]
                            if re.findall(self.pattern_no, event2.obj.message['text'], flags=re.IGNORECASE):
                                message_no = "Как знаешь.\nЕсли что, я тут, обращайся"
                                self.write_msg(user_id=companion_user.user_id, message=message_no)
                            if re.findall(self.pattern_yes, event2.obj.message['text'], flags=re.IGNORECASE):
                                self.write_msg(user_id=companion_user.user_id, message="Тогда проиступим!")
                                self.user_id = companion_user.user_id
                                return [companion_user.user_id, "Have dialog."]

        return ['-1', 'Error']

    # Вопрос-ответ
    def ask_user(self, message) -> str:
        self.write_msg(user_id=self.user_id, message=message)
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                pprint(event.object.message)
                return event.obj.message['text']

    # Проверяем возраст на адекватность
    @staticmethod
    def is_age_valid(user_answer: str):
        if user_answer.isdigit() and int(user_answer) > 0 and int(user_answer) <= 120:
            return True
        else:
            return False

    # Получение данных для формирования списка кандадатов
    def get_data_4_candidates_list(self):

        self.write_msg(user_id=self.user_id,
                       message="Теперь мне потребуются некоторые входные данные:\n"
                               " - возрастной интервал кандидатов (минимальный и максимальный возраст;\n"
                               " - город их проживания."
                               "Продолжим?")

        still_in_dialog = False  # Флаг на случай, если что пойдёт не так

        for i in range(10):
            match self.get_user_opinion():
                case 'Yes':
                    still_in_dialog = True
                    break
                case 'No':
                    break
                case 'Unknown':
                    pass

        # Если клиент таки отказался от диалога
        if not still_in_dialog:
            return 'Fail'

        # Продолжаем разговор

        user_answer = self.ask_user("Напиши минамальный возраст кандидата:")
        if not self.is_age_valid(user_answer):
            still_in_dialog = False
            for i in range(10):
                user_answer = self.ask_user("Извини,  с возрастом что-то не так:")
                if self.is_age_valid(user_answer):
                    still_in_dialog = True
                    break
        if not still_in_dialog:
            return 'Fail'
        else:
            min_age = user_answer

        user_answer = self.ask_user("Напиши максимальный возраст кандидата:")
        if not self.is_age_valid(user_answer):
            still_in_dialog = False
            for i in range(10):
                user_answer = self.ask_user("Извини,  с возрастом что-то не так:")
                if self.is_age_valid(user_answer):
                    still_in_dialog = True
                    break
        if not still_in_dialog:
            return 'Fail'
        else:
            max_age = user_answer

        if min_age > max_age:
            min_age, max_age = max_age, min_age

        user_answer = self.ask_user("Напиши город, где живёт кандидат:")
        city_name = user_answer

        data_base = DataBaseExchange()

        return data_base.get_candidates(min_age=int(min_age), max_age=int(max_age), city_name=city_name)

    def get_user_opinion(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                pprint(event.object.message)

                companion_user = Person(event.object.message['from_id'])

                if event.obj.message['text'] == 'изыди':
                    self.write_msg(user_id=companion_user.user_id, message="Как скажете.")
                    return 'Canceled by user.'
                elif re.findall(self.pattern_no, event.obj.message['text'], flags=re.IGNORECASE):
                    message_no = "Как знаешь.\nЕсли что, я тут, обращайся"
                    self.write_msg(user_id=companion_user.user_id, message=message_no)
                    return 'No'
                elif re.findall(self.pattern_yes, event.obj.message['text'], flags=re.IGNORECASE):
                    self.write_msg(user_id=companion_user.user_id, message='Ok')
                    return 'Yes'
                else:
                    message_bad = 'Извини, не понял. Повтори пожалуйста.'
                    self.write_msg(user_id=companion_user.user_id, message=message_bad)

    def person_list_presentation(self, pers_list: list):
        pers_st = PersonListStack(pers_list)

        while not pers_st.is_empty():
            next_person = pers_st.get_next()

            user = Person(next_person)
            self.write_msg(user)
            self.write_msg(user.get_photos_of_person_4_attach(next_person))

            self.write_msg('Следующий?')
            if self.get_user_opinion() == 'No':
                self.write_msg('Может в следующий раз?')
                pers_st.clean()
                return 'Canceled'

        return 'Complete'


