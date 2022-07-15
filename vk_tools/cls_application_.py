import re
from vk_api import VkApi
from random import randrange
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from cls.cls_person_list_iteration import PersonListStack
import json

from pprint import pprint

from cls.cls_Person import Person
from cls.cls_DataBaseExchange import DataBaseExchange
from tokens.cls_tokens import Token
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

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

        token = Token()
        self.GROUP_ID = token.app_dict['APPLICATION']['GROUP_ID']
        self.GROUP_TOKEN = token.app_dict['APPLICATION_TOKENS']['GROUP_TOKEN']
        self.API_VERSION = token.app_dict['APPLICATION']['API_VERSION']
        self.APPLICATION_TOKEN = token.app_dict['APPLICATION_TOKENS']['APPLICATION_TOKEN']
        self.OWNER_ID = token.app_dict['APPLICATION']['OWNER_ID']

    # Send messages
    def write_msg(self, message, user_id='default'):
        if user_id == 'default':
            user_id = self.user_id
        self.vk_session.method('messages.send',
                               {'user_id': int(user_id), 'message': message, 'random_id': randrange(10 ** 7)})

    # The new user dialog cycle
    def new_companion(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                companion_user = Person(event.object.message['from_id'])

                if event.obj.message['text'] == 'изыди':
                    self.write_msg(user_id=companion_user.user_id, message="Как скажете.")
                    return [companion_user.user_id, "Canceled by user."]
                elif re.findall(self.pattern_hi, event.obj.message['text'], flags=re.IGNORECASE):
                    message_good = f"Здаров, коль не шутишь! {companion_user.first_name}, " \
                                   f"предлагаю тебе попробовать познакомиться с кем-нибудь. Согласен? :)"
                    self.write_msg(user_id=companion_user.user_id, message=message_good)

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
            match self.get_user_opinion():
                case 'Yes':
                    still_in_dialog = True
                    break
                case 'No':
                    break
                case 'Unknown':
                    pass

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

    def write_msg(self, message, user_id='default'):
        if user_id == 'default':
            user_id = self.user_id
        self.vk_session.method('messages.send',
                               {'user_id': int(user_id), 'message': message, 'random_id': randrange(10 ** 7)})

    def write_photo_msg(self, message, photo_ident, menu, user_id='default'):
        if user_id == 'default':
            user_id = self.user_id
        self.vk_session.method('messages.send',{'user_id': int(user_id), 'message': message, "keyboard": menu, "attachment": photo_ident,
                            'random_id': randrange(10 ** 7)})

    def partner_menu(self, partner_person):
        favorites_dict = {}
        black_dict = {}
        self.partner_person = partner_person
        partner_full_name = f"{self.partner_person['first_name']} {self.partner_person['last_name']}"
        companion_user = Person(self.user_id)
        CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')
        settings = dict(one_time=False, inline=True)
        menu_1 = VkKeyboard(**settings)
        menu_1.add_callback_button(label='В избранное', color=VkKeyboardColor.POSITIVE,
                                       payload={"type": "add_to_favor"})
        menu_1.add_callback_button(label='В чёрный список', color=VkKeyboardColor.NEGATIVE,
                                       payload={"type": "add_to_blacklist"})
        menu_1.add_callback_button(label='Следующий', color=VkKeyboardColor.PRIMARY,
                                       payload={"type": "next"})
        menu_1.add_callback_button(label='Откртыть избранных', color=VkKeyboardColor.PRIMARY,
                                       payload={"type": "open_favor"})
        self.vk.messages.send(user_id=companion_user.user_id, random_id=randrange(10 ** 7),
                                  peer_id=companion_user.user_id, keyboard=menu_1.get_keyboard(),
                                  message=self.partner_person['link'])

        menu_2 = VkKeyboard(**settings)
        menu_2.add_callback_button(label='Сочный лайк', color=VkKeyboardColor.POSITIVE, payload={"type": "like"})
        menu_2.add_callback_button(label='Отменить лайк', color=VkKeyboardColor.NEGATIVE, payload={"type": "return_like"})
        menu_2.add_callback_button(label='Назад к знакомствам', color=VkKeyboardColor.PRIMARY, payload={"type": "return_to_dating"})

        for event_menu1 in self.longpoll.listen():
            if event_menu1.type == VkBotEventType.MESSAGE_EVENT:
                if event_menu1.object.payload.get('type') == 'add_to_favor':
                    favorites_dict[self.partner_person['user_id']] = [partner_full_name, self.partner_person['photo_ident'], self.partner_person['link']]

                elif event_menu1.object.payload.get('type') == 'add_to_blacklist':
                    black_dict[self.partner_person('user_id')] = [partner_full_name, self.partner_person['photo_ident'], self.partner_person['link']]
                elif event_menu1.object.payload.get('type') == 'next':
                    return
                elif event_menu1.object.payload.get('type') == 'open_favor':
                    self.write_msg("......::::::ИЗБРАННЫЕ::::::......", user_id='default')
                    for id, person in favorites_dict.items():
                        message = f"{person[0]}\n{person[2]}"
                        self.write_photo_msg(message, person[1], menu_2.get_keyboard())
                        for event_menu2 in self.longpoll.listen():
                            if event_menu2.type == VkBotEventType.MESSAGE_EVENT:
                                if event_menu2.object.payload.get('type') == 'like':
                                    self.vk.likes.add(type='photo', owner_id=id, item_id=partner_person['photo_id'])
                                if event_menu2.object.payload.get('type') == 'return_like':
                                    self.vk.likes.delete(type='photo', owner_id=id, item_id=partner_person['photo_id'])
                                if event_menu2.object.payload.get('type') == 'return_to_dating':
                                    return

    def person_list_presentation(self, pers_list: list):
        pers_st = PersonListStack(pers_list)

        while not pers_st.is_empty():
            next_person = pers_st.get_next()

            partner_person = {}
            user = Person(next_person)
            partner_person['user_id'] = user.user_id
            partner_person['first_name'] = user.first_name
            partner_person['last_name'] = user.last_name
            partner_person['age'] = user.age
            partner_person['link'] = f"https://vk.com/id{partner_person['user_id']}"


            # !!!!!!!!partner_person['photo_ident'] = "photo218659720_340765211"
            # !!!!!!!!partner_person['photo_id'] = "340765211"
            # планировал их взять из """Дык не вопрос.. Завтра гляну. Могу вернуть словарь.Id: URL
            #                             Александр Садовой — Сегодня, в 0:50 там одним из параметров будет id?
            #                             Ключем. Переменная- URL"""

            self.write_msg(user)
            self.write_msg(user.get_photos_of_person_4_attach(next_person))
            self.partner_menu(partner_person)

        return 'Complete'
