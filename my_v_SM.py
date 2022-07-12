# import vk_api
# import os
import json
import re
import csv
import requests
import sqlalchemy
from vk_api import VkApi
from cls.cls_Person import Person
from random import randrange
from main import get_personal_data
# from cls_HttpReq import HttpR
# from cls_VkUrl import VkUrl
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from pprint import pprint
import pathlib
from pathlib import Path
import configparser

from cls.cls_Person import Person


class Application:
    GROUP_ID = ()
    GROUP_TOKEN = ()
    API_VERSION = ()
    APP_ID = ()
    APPLICATION_TOKEN = ()
    OWNER_ID = ()
    CALLBACK_TYPES = ['show_snackbar', 'open_link', 'open_app']

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
    def write_msg(self, companion_id, message):
        self.vk_session.method('messages.send',
                               {'user_id': companion_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def new_companion(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                pprint(event.object.message)

                companion_user = Person(event.object.message['from_id'])

                pattern_hi = "(прив)|(хай)|(здаров)|(салам)|(здравст)|(добр..)|(салют)|(ку)|(hi)|(ghbd)|(\[fq)"
                pattern_no = "(не)|(нет)|(нехочу)|(не хочу)|(no)|(ne)|(not)(\[fq)"

                if event.obj.message['text'] == 'изыди':
                    self.write_msg(companion_user.user_id, "Как скажете.")
                    return "Canceled by user."
                elif re.findall(pattern_hi, event.obj.message['text'], flags=re.IGNORECASE):
                    message_good = f"Здаров, коль не шутишь! {companion_user.first_name}, предлагаю тебе попробовать познакомиться с кем-нибудь. Согласен? :)"
                    self.write_msg(companion_user.user_id, message_good)
                elif re.findall(pattern_no, event.obj.message['text'], flags=re.IGNORECASE):
                    message_no = "Как знаешь.\nЕсли что, я тут, обращайся"
                    self.write_msg(companion_user.user_id, message_no)
                else:
                    message_bad = f"Не здороваюсь.... {companion_user.last_name}, будешь знакомиться с кем-нибудь?"
                    self.write_msg(companion_user.user_id, message_bad)

        return companion_user.user_id


bot = Application()
print(bot.new_companion())
