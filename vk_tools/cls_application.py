import re
from vk_api import VkApi, VkUpload
from random import randrange
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from cls.cls_Person import Person
from tokens.cls_tokens import Token

from cls.cls_DataBaseExchange import DataBaseExchange
from cls.cls_json import Add2Json

from pprint import pprint

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
    pattern_no = "(не)|(нет)|(нехочу)|(не хочу)|(no)|(ne)|(not)|(n)"
    pattern_yes = "(давай)|(да)|(ок)|(хорош)|(соглас)|(добро)|(ладно)|(yes)|(lf)|(yep)|(замётано)|(y)"
    pattern_next = "(следующий)|(next)|(давай ещё)"
    pattern_favorite = "(нравится)|(добавить в избранное)|(прикольно)|(выбираю)|(favorite)|(to favorites)|(add)"
    pattern_end = "(нет)|(хватит)|(заканчивай)|(хрень)|(end)|(quit)|(esqape)|(escape)|(q)|(esc)"

    flag_stop = False

    message_id_list = []

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

    def delete_messages(self):
        print(f'Delete messages: {self.message_id_list}')
        self.vk.messages.delete(delete_for_all=1, message_ids=self.message_id_list)
        self.message_id_list.clear()

    def get_external_call(self):
        for event in self.longpoll.listen():
            print(f'event.type: {event.type}')
            print(f'event.object: {event.object}')
            pprint(event.object)
            if event.type == VkBotEventType.MESSAGE_REPLY:
                self.message_id_list.append(event.object['conversation_message_id'])
            if event.type == VkBotEventType.MESSAGE_EVENT:
                self.message_id_list.append(event.object['conversation_message_id'])
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.message_id_list.append(event.obj.message['conversation_message_id'])
            if event.type == VkBotEventType.MESSAGE_NEW:
                companion_user = Person(event.object.message['from_id'])
                print(f'companion_user: {companion_user}')
                return companion_user.user_id, event.obj.message['text'], 'text'
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                companion_user = Person(event.object['user_id'])
                if event.object.payload.get('type') == 'next':

                    mess = self.vk.messages.getHistory(user_id=companion_user.user_id, count=200, offset=0)['items']
                    ids_messages = []
                    for element in mess:
                        if element['text'] == "Теперь посмотрим кого удалось отыскать.":
                            break
                        else:
                            ids_messages.append(str(element['id']))
                    ids_messages = ','.join(ids_messages)
                    self.vk.messages.delete(delete_for_all=1, message_ids=ids_messages)

                return companion_user.user_id, event.object.payload.get('type'), 'button'

    def write_msg(self, message, user_id='default', attachment=''):
        if user_id == 'default':
            user_id = self.user_id
        self.vk_session.method('messages.send',
                               {'user_id': int(user_id),
                                'message': message,
                                'random_id': randrange(10 ** 7),
                                'attachment': attachment})

    def wellcome(self, user_id, message):
        companion_user = Person(user_id)
        if re.findall(self.pattern_hi, message, flags=re.IGNORECASE):
            message = f"Здаров, коль не шутишь! {companion_user.first_name}, " \
                           f"предлагаю тебе попробовать познакомиться с кем-нибудь. Согласен? :)"
        else:
            message = f"Не здороваюсь.... {companion_user.last_name}, будешь знакомиться с кем-нибудь?"

        self.ask_user_yes_no(user_id=companion_user.user_id, message=message)

    def ask_user_yes_no(self, message, user_id='default'):
        if user_id == 'default':
            user_id = self.user_id
        settings = dict(one_time=False, inline=True)
        menu_1 = VkKeyboard(**settings)
        menu_1.add_callback_button(label='Да', color=VkKeyboardColor.POSITIVE, payload={"type": "yes"})
        menu_1.add_callback_button(label='Нет', color=VkKeyboardColor.NEGATIVE, payload={"type": "no"})

        self.vk.messages.send(user_id=user_id, random_id=randrange(10 ** 7),
                              peer_id=user_id, keyboard=menu_1.get_keyboard(),
                              message=message)

    def ask_user_about_candidate(self, message, user_id='default'):
        if user_id == 'default':
            user_id = self.user_id
        settings = dict(one_time=False, inline=True)
        menu_1 = VkKeyboard(**settings)
        menu_1.add_callback_button(label='В избранное', color=VkKeyboardColor.POSITIVE, payload={"type": "add_to_favor"})

        menu_1.add_line()
        menu_1.add_callback_button(label='Следующий', color=VkKeyboardColor.PRIMARY,
                                   payload={"type": "next"})
        menu_1.add_callback_button(label='Закончить', color=VkKeyboardColor.NEGATIVE,
                                   payload={"type": "complete"})

        self.vk.messages.send(user_id=user_id, random_id=randrange(10 ** 7),
                              peer_id=user_id, keyboard=menu_1.get_keyboard(),
                              message=message)

    def get_user_opinion(self, user_id, message):
        if re.findall(self.pattern_no, message, flags=re.IGNORECASE):
            return 'No'
        elif re.findall(self.pattern_yes, message, flags=re.IGNORECASE):
            self.write_msg(user_id=user_id, message='Ok')
            return 'Yes'
        else:
            message_bad = 'Извини, не понял. Повтори пожалуйста.'
            self.write_msg(user_id=user_id, message=message_bad)

    def check_user_opinion_in_presentation(self, message, user_id='default'):
        if user_id == 'default':
            user_id = self.user_id
        if re.findall(self.pattern_favorite, message, flags=re.IGNORECASE):
            return 'add_to_favor'
        elif re.findall(self.pattern_end, message, flags=re.IGNORECASE):
            return 'complete'
        elif re.findall(self.pattern_next, message, flags=re.IGNORECASE):
            return 'next'
        else:
            message_bad = 'Извини, не понял. Повтори пожалуйста.'
            self.write_msg(user_id=user_id, message=message_bad)

    @staticmethod
    def is_age_valid(user_answer: str):
        if user_answer.isdigit() and int(user_answer) > 0 and int(user_answer) <= 120:
            return True
        else:
            return False

    def person_presentation(self, user_id, candidate_id):
        candidate = Person(candidate_id)
        data_base = DataBaseExchange()

        photos_id_list, photos_list = data_base.get_photo_from_db(candidate.user_id)

        if len(photos_id_list) == 0:
            print('No photo in DataBase. Look at photos on VK.')
            photos_list, photos_id_list = self.get_photo_list_from_VK(candidate.user_id)

        attach = f"{''.join([f'photo{candidate.user_id}_{photo_id},' for photo_id in photos_id_list])}"[
                 :-1]
        self.write_msg(user_id=user_id, message=candidate, attachment=attach)

    def person_presentation_f_json(self, user_id, candidate_id):

        add_jeson = Add2Json('db_in_json.json')

        user_data, photos_id_list = add_jeson.get_candidate_data_fron_json(candidate_id)

        message = f"{user_data['first_name']} " \
                   f"{user_data['last_name']}" \
                   f"\n{user_data['url']}"

        if len(photos_id_list) == 0:
            print('No photo in json. Look at photos on VK.')
            photos_list, photos_id_list = self.get_photo_list_from_VK(candidate_id)

        attach = f"{''.join([f'photo{candidate_id}_{photo_id},' for photo_id in photos_id_list])}"[
                 :-1]
        self.write_msg(user_id=user_id, message=message, attachment=attach)

    def get_photo_list_from_VK(self, user_id):
        user = Person(user_id)

        photos_list = user.get_photos_of_person(user_id)
        photos_id_list = user.photo_id_list

        return photos_list, photos_id_list
