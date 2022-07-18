import re
from vk_api import VkApi, VkUpload
from random import randrange
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from cls.cls_Person import Person
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

    def get_external_call(self):
        for event in self.longpoll.listen():
            print('new_companion cycle')
            if event.type == VkBotEventType.MESSAGE_NEW:
                companion_user = Person(event.object.message['from_id'])
                print(f'companion_user: {companion_user.user_id}')

                return companion_user.user_id, event.obj.message['text']

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
            message_good = f"Здаров, коль не шутишь! {companion_user.first_name}, " \
                           f"предлагаю тебе попробовать познакомиться с кем-нибудь. Согласен? :)"
            self.write_msg(user_id=companion_user.user_id, message=message_good)
        else:
            message_bad = f"Не здороваюсь.... {companion_user.last_name}, будешь знакомиться с кем-нибудь?"
            self.write_msg(user_id=companion_user.user_id, message=message_bad)

    def get_user_opinion(self, user_id, message):
        if re.findall(self.pattern_no, message, flags=re.IGNORECASE):
            return 'No'
        elif re.findall(self.pattern_yes, message, flags=re.IGNORECASE):
            self.write_msg(user_id=user_id, message='Ok')
            return 'Yes'
        else:
            message_bad = 'Извини, не понял. Повтори пожалуйста.'
            self.write_msg(user_id=user_id, message=message_bad)

    @staticmethod
    def is_age_valid(user_answer: str):
        if user_answer.isdigit() and int(user_answer) > 0 and int(user_answer) <= 120:
            return True
        else:
            return False
