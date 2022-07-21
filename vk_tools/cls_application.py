from random import randrange
from pprint import pprint

import vk_api.exceptions
from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from cls.cls_Person import Person
from tokens.cls_tokens import Token
from cls.cls_DataBaseExchange import DataBaseExchange
from cls.cls_json import Add2Json

# This class divided by three modules
from vk_tools.Lib import add_functions_as_methods
from vk_tools.bot_cycle import bot_cycle
from vk_tools.speak_with_user import wellcome, ask_user_yes_no, ask_user_about_candidate, ask_user_after_favor
from vk_tools.speak_with_user import get_user_opinion, check_user_opinion_in_presentation, check_user_opinion_


# Connection external modules to class
@add_functions_as_methods(bot_cycle, wellcome, ask_user_yes_no, ask_user_about_candidate, ask_user_after_favor,
                          get_user_opinion, check_user_opinion_in_presentation, check_user_opinion_)
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

        self.take_application_data()  # get security and application data

        if len(self.GROUP_ID) == 0:
            print(f'Error read {db_data_file_path}')
        else:
            self.vk_session = VkApi(token=self.GROUP_TOKEN, api_version=self.API_VERSION)
            self.vk = self.vk_session.get_api()
            self.upload = VkUpload(self.vk_session)

            # To use Long Poll API
            self.longpoll = VkBotLongPoll(self.vk_session, group_id=self.GROUP_ID)

    def take_application_data(self):
        """
        Get security and application data from class Token
        """

        token = Token()
        self.GROUP_ID = token.app_dict['APPLICATION']['GROUP_ID']
        self.GROUP_TOKEN = token.app_dict['APPLICATION_TOKENS']['GROUP_TOKEN']
        self.API_VERSION = token.app_dict['APPLICATION']['API_VERSION']
        self.APPLICATION_TOKEN = token.app_dict['APPLICATION_TOKENS']['APPLICATION_TOKEN']
        self.OWNER_ID = token.app_dict['APPLICATION']['OWNER_ID']

    def delete_messages(self, user_id='default'):
        """
        Cleans dialog
        :param user_id: user identification number
        """
        if user_id == 'default':
            user_id = self.user_id
        print(f'Delete messages: {self.message_id_list}')

        mess = self.vk.messages.getHistory(user_id=user_id, count=200, offset=0)['items']
        ids_messages = []
        for element in mess:
            if element['text'] == "Теперь посмотрим кого удалось отыскать.":
                break
            else:
                ids_messages.append(str(element['id']))
        ids_messages = ','.join(ids_messages)

        try:
            self.vk.messages.delete(delete_for_all=1, message_ids=ids_messages)
        except vk_api.exceptions.ApiError:
            print("Messages can not be deleted.")

    def get_external_call(self):
        """
        Listening users connections to application
        :return: companion_user.user_id: user identification number,
                event.obj.message['text']: text of user message,
                'text' or 'button' depends of event type

        """

        for event in self.longpoll.listen():
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

                return companion_user.user_id, event.object.payload.get('type'), 'button'

    def write_msg(self, message, user_id='default', attachment=''):
        """
        Writes messages to user dialog
        :param message: text of message
        :param user_id: user identification number
        :param attachment: String of parameters to show user photos
        """
        if user_id == 'default':
            user_id = self.user_id
        self.vk_session.method('messages.send',
                               {'user_id': int(user_id),
                                'message': message,
                                'random_id': randrange(10 ** 7),
                                'attachment': attachment})

    @staticmethod
    def is_age_valid(user_answer: str):
        """
        Just checks if user gave an age adequate for next search
        """
        if user_answer.isdigit() and 0 < int(user_answer) <= 120:
            return True
        else:
            return False

    def person_presentation(self, user_id, candidate_id):
        """
        Outputs some candidate data from DatBase to present
        :param user_id: user identification number
        :param candidate_id: identification of other person, whose data user pretend to get
        """
        candidate = Person(candidate_id)
        data_base = DataBaseExchange()

        photos_id_list, photos_list = data_base.get_photo_from_db(candidate.user_id)

        if len(photos_id_list) == 0:
            print('No photo in DataBase. Look at photos on VK.')
            photos_list, photos_id_list = self.get_photo_list_from_vk(candidate.user_id)

        attach = f"{''.join([f'photo{candidate.user_id}_{photo_id},' for photo_id in photos_id_list])}"[
                 :-1]
        self.write_msg(user_id=user_id, message=candidate, attachment=attach)

    def person_presentation_f_json(self, user_id, candidate_id):
        """
        Outputs some candidate data from json storage file to present
        :param user_id: user identification number
        :param candidate_id: identification of other person, whose data user pretend to get
        """
        add_jeson = Add2Json('db_in_json.json')

        user_data, photos_id_list = add_jeson.get_candidate_data_fron_json(candidate_id)

        message = f"{user_data['first_name']} " \
                  f"{user_data['last_name']}" \
                  f"\n{user_data['url']}"

        if len(photos_id_list) == 0:
            print('No photo in json. Look at photos on VK.')
            photos_list, photos_id_list = self.get_photo_list_from_vk(candidate_id)

        attach = f"{''.join([f'photo{candidate_id}_{photo_id},' for photo_id in photos_id_list])}"[
                 :-1]
        self.write_msg(user_id=user_id, message=message, attachment=attach)

    @staticmethod
    def get_photo_list_from_vk(user_id):
        """
        Gets user photo from VK by user identification number
        :param user_id:user identification number
        :return: photos_list: list of photos,
                 photos_id_list: list of photos identification numbers
        """
        user = Person(user_id)

        photos_list = user.get_photos_of_person(user_id)
        photos_id_list = user.photo_id_list

        return photos_list, photos_id_list

    def get_personal_data(self, user_id: str, write_2_json: str):
        """
        Get account data from VK by an identification number
        :param user_id: account identification number
        :param write_2_json: 'y'- if user pretend to save dato to json
        """
        user = Person(str(user_id))
        print()

        data_base = DataBaseExchange()

        if user.data_are_good:
            user_dict = user.get_person_data()
            print('Version for Database:')
            pprint(user_dict)
            data_base.add_user_data(user_dict)

            print('Take data from VK.')
            photos_list, photos_id_list = self.get_photo_list_from_vk(user_id)
            data_base.add_user_photos(user_dict, photos_list, photos_id_list)

            if write_2_json == 'y':
                user_dict.setdefault('photos_id_list', photos_id_list)
                print('\nPerson data saved in json file')

                add_jeson = Add2Json('db_in_json.json')
                add_jeson.add_2_json(user_id, user_dict)
            else:
                print('Person data in DataBase only.')

        else:
            print('The person data are not useful.')

    @staticmethod
    def get_photo_list_from_db(user_id):
        """
        Gets user photo from DataBase by user identification number
        :param user_id: user identification number
        :return: photos_list: list of photos,
                 photos_id_list: list of photos identification numbers
        """
        data_base = DataBaseExchange()
        print('Get data from DB:')
        photos_id_list, photos_list = data_base.get_photo_from_db(user_id)

        return photos_list, photos_id_list
