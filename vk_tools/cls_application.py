import re
from vk_api import VkApi, VkUpload
from random import randrange
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from cls.cls_person_list_iteration import PersonListStack

from pprint import pprint

from cls.cls_Person import Person
from cls.cls_DataBaseExchange import DataBaseExchange
from tokens.cls_tokens import Token


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

    flag_stop = False

    def __init__(self, db_data_file_path='/tokens/application_data.ini'):
        self.take_application_data(db_data_file_path)

        if len(self.GROUP_ID) == 0:
            print(f'Error read {db_data_file_path}')
        else:
            self.vk_session = VkApi(token=self.GROUP_TOKEN, api_version=self.API_VERSION)
            self.vk = self.vk_session.get_api()
            self.upload = VkUpload(self.vk_session)


            # To use Long Poll API
            self.longpoll = VkBotLongPoll(self.vk_session, group_id=self.GROUP_ID)

    def take_application_data(self, db_data_file_path):

        token = Token()
        self.GROUP_ID = token.app_dict['APPLICATION']['GROUP_ID']
        self.GROUP_TOKEN = token.app_dict['APPLICATION_TOKENS']['GROUP_TOKEN']
        self.API_VERSION = token.app_dict['APPLICATION']['API_VERSION']
        self.APPLICATION_TOKEN = token.app_dict['APPLICATION_TOKENS']['APPLICATION_TOKEN']
        self.OWNER_ID = token.app_dict['APPLICATION']['OWNER_ID']

    # Send messages
    # def write_msg(self, message, user_id='default'):
    #     if user_id == 'default':
    #         user_id = self.user_id
    #     self.vk_session.method('messages.send',
    #                            {'user_id': int(user_id), 'message': message, 'random_id': randrange(10 ** 7)})

    def write_msg(self, message, user_id='default', attachment=''):
        if user_id == 'default':
            user_id = self.user_id
        self.vk_session.method('messages.send',
                               {'user_id': int(user_id),
                                'message': message,
                                'random_id': randrange(10 ** 7),
                                'attachment': attachment})


    # The new user dialog cycle
    def new_companion(self):
        for event in self.longpoll.listen():
            print('new_companion cycle')
            if event.type == VkBotEventType.MESSAGE_NEW:
                companion_user = Person(event.object.message['from_id'])
                print(f'companion_user: {companion_user.user_id}')

                if event.obj.message['text'] == 'изыди':
                    self.write_msg(user_id=companion_user.user_id, message="Как скажете.")
                    self.flag_stop = True
                    return [companion_user.user_id, "Canceled by user."]
                elif re.findall(self.pattern_hi, event.obj.message['text'], flags=re.IGNORECASE):
                    message_good = f"Здаров, коль не шутишь! {companion_user.first_name}, " \
                                   f"предлагаю тебе попробовать познакомиться с кем-нибудь. Согласен? :)"
                    self.write_msg(user_id=companion_user.user_id, message=message_good)

                    for event2 in self.longpoll.listen():
                        if event2.type == VkBotEventType.MESSAGE_NEW:

                            if event2.obj.message['text'] == 'изыди':
                                self.write_msg(user_id=companion_user.user_id, message="Как скажете.")
                                # return [companion_user.user_id, "Canceled by user."]
                                return [companion_user.user_id, "Stop"]

                            elif re.findall(self.pattern_no, event2.obj.message['text'], flags=re.IGNORECASE):
                                message_no = "Как знаешь.\nЕсли что, я тут, обращайся"
                                self.write_msg(user_id=companion_user.user_id, message=message_no)
                                return [companion_user.user_id, "Canceled"]

                            elif re.findall(self.pattern_yes, event2.obj.message['text'], flags=re.IGNORECASE):
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

                            elif re.findall(self.pattern_no, event2.obj.message['text'], flags=re.IGNORECASE):
                                message_no = "Как знаешь.\nЕсли что, я тут, обращайся"
                                self.write_msg(user_id=companion_user.user_id, message=message_no)

                            elif re.findall(self.pattern_yes, event2.obj.message['text'], flags=re.IGNORECASE):
                                self.write_msg(user_id=companion_user.user_id, message="Тогда проиступим!")
                                self.user_id = companion_user.user_id
                                return [companion_user.user_id, "Have dialog."]

        return ['-1', 'Error']

    # Ask user - get response
    def ask_user(self, message) -> str:
        self.write_msg(user_id=self.user_id, message=message)
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                pprint(event.object.message)
                return event.obj.message['text']

    # Check if user age is adequate
    @staticmethod
    def is_age_valid(user_answer: str):
        if user_answer.isdigit() and int(user_answer) > 0 and int(user_answer) <= 120:
            return True
        else:
            return False

    # Get data for candidate list formation
    def get_data_4_candidates_list(self):

        self.write_msg(user_id=self.user_id,
                       message="Теперь мне потребуются некоторые входные данные:\n"
                               " - возрастной интервал кандидатов (минимальный и максимальный возраст;\n"
                               " - город их проживания.\n"
                               "Продолжим?")

        still_in_dialog = False  # insurance flag

        for i in range(10):
            print('for i in range(10)')
            match self.get_user_opinion():
                case 'Yes':
                    print("case 'Yes'")
                    still_in_dialog = True
                    break
                case 'No|Canceled by user.':
                    print("case 'No'")
                    break
                case 'Unknown':
                    print("case 'Unknown'")
                    pass

        if self.flag_stop:
            return 'Stop'

        # if user canceled the dialog
        if not still_in_dialog:
            return 'Fail'

        # continue dialog
        user_answer = self.ask_user("Напиши минамальный возраст кандидата:")
        if not self.is_age_valid(user_answer):
            still_in_dialog = False

            for i in range(10):
                user_answer = self.ask_user("Извини,  с возрастом что-то не так:")

                if self.is_age_valid(user_answer):
                    still_in_dialog = True
                    break

        if self.flag_stop:
            return 'Stop'

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
            # self.write_msg(user.get_photos_of_person_4_attach(next_person))
            # print(user.photo_id_list)


            data_base = DataBaseExchange()
            photos_id_list, photos_list = data_base.get_photo_from_db(user.user_id)

            attach = f"{''.join([f'photo{user.user_id}_{photo_id},' for photo_id in photos_list])}"[:-1]
            print(f'attach: {attach}')
            self.write_msg(user, attachment=attach)


            # self.write_msg(photos_list)
            # self.upload_photo(photos_id_list)

            self.write_msg('Следующий?')
            if self.get_user_opinion() != 'Yes':
                self.write_msg('Как скажешь.')
                pers_st.clean()
                if self.flag_stop:
                    return 'Stop'
                return 'Canceled'

        return 'Complete'
