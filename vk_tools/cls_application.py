from random import randrange
import vk_api.exceptions
from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from cls.cls_Person import Person
from tokens.cls_tokens import Token
# This class divided by three modules
from vk_tools.Lib import add_functions_as_methods
from vk_tools.bot_cycle import bot_cycle
from vk_tools.speak_with_user import wellcome, \
    ask_user_yes_no, ask_user_about_candidate, ask_user_after_favor
from vk_tools.speak_with_user import get_user_opinion, \
    check_user_opinion_in_presentation, check_user_opinion_

"""Connection of external modules to class"""


@add_functions_as_methods(check_user_opinion_in_presentation, wellcome,
                          ask_user_about_candidate, ask_user_yes_no,
                          get_user_opinion, ask_user_after_favor, bot_cycle,
                          check_user_opinion_)
class Application:
    user_id = ()
    GROUP_ID = ()
    GROUP_TOKEN = ()
    API_VERSION = ()
    APP_ID = ()
    APPLICATION_TOKEN = ()
    OWNER_ID = ()
    CALLBACK_TYPES = ['show_snackbar', 'open_link', 'open_app']
    pattern_hi = "(прив)|(хай)|(здаров)|(салам)|(здравст)|(добр..)|(салют)|(ку)|(hi)|(ghbd)"
    pattern_no = "(не)|(нет)|(нехочу)|(не хочу)|(no)|(ne)|(not)|(n)"
    pattern_yes = "(давай)|(да)|(ок)|(хорош)|(соглас)|(добро)" \
                  "|(ладно)|(yes)|(lf)|(yep)|(замётано)|(y)"
    pattern_next = "(следующий)|(next)|(давай ещё)"
    pattern_favorite = "(нравится)|(добавить в избранное)|(прикольно)" \
                       "|(выбираю)|(favorite)|(to favorites)|(add)"
    pattern_end = "(нет)|(хватит)|(заканчивай)|(хрень)|(end)|(quit)" \
                  "|(esqape)|(escape)|(q)|(esc)"
    flag_stop = False
    message_id_list = []

    def __init__(self, db_data_file_path='/tokens/application_data.ini'):
        """Get security and application data"""
        self.take_application_data()
        if len(self.GROUP_ID) == 0:
            print(f'Error read {db_data_file_path}')
        else:
            self.vk_session = VkApi(token=self.GROUP_TOKEN, api_version=self.API_VERSION)
            self.vk = self.vk_session.get_api()
            self.upload = VkUpload(self.vk_session)
            # To use Long Poll API
            self.longpoll = VkBotLongPoll(self.vk_session, group_id=self.GROUP_ID)

    def take_application_data(self):
        """Get security and application data from class Token"""
        token = Token()
        self.GROUP_ID = token.app_dict['APPLICATION']['GROUP_ID']
        self.GROUP_TOKEN = token.app_dict['APPLICATION_TOKENS']['GROUP_TOKEN']
        self.API_VERSION = token.app_dict['APPLICATION']['API_VERSION']
        self.APPLICATION_TOKEN = token.app_dict['APPLICATION_TOKENS']['APPLICATION_TOKEN']
        self.OWNER_ID = token.app_dict['APPLICATION']['OWNER_ID']

    def delete_messages(self, user_id='default'):
        """Cleans dialog: param user_id: user identification number"""
        if user_id == 'default':
            user_id = self.user_id
        mess = self.vk.messages.getHistory(user_id=user_id,
                                           count=200, offset=0)['items']
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
        """Listening users connections to application:
        return:
        companion_user.user_id: user identification number,
        event.obj.message['text']:text of user message,
        'text' or 'button' depends of event type.
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
        """Writes messages to user dialog param:
        message: text of message
        user_id: user identification number
        attachment: string of parameters to show user photos
        """
        if user_id == 'default':
            user_id = self.user_id
        self.vk_session.method('messages.send', {
            'user_id': int(user_id),
            'message': message,
            'random_id': randrange(10 ** 7),
            'attachment': attachment
        }
                               )

    @staticmethod
    def is_age_valid(user_answer: str):
        """Just checks if user gave an age adequate for next search"""
        if user_answer.isdigit() and 0 < int(user_answer) <= 120:
            return True
        else:
            return False

    def person_presentation_f_vk(self, user_id, candidate_id):
        """Outputs some candidate data from json storage file to present param:
        user_id: user identification number
        candidate_id: identification of other person,
        whose data user pretend to get
        """
        pers = Person(candidate_id)

        user_data = pers.get_person_data()
        message = f"{user_data['first_name']} " \
                  f"{user_data['last_name']}" \
                  f"\n{user_data['url']}"
        photos_list, photos_id_list = self.get_photo_list_from_vk(candidate_id)
        attach = f"""{''.join([f'photo{candidate_id}_{photo_id},'
                               for photo_id in photos_id_list])}"""[:-1]
        self.write_msg(user_id=user_id, message=message, attachment=attach)

    @staticmethod
    def get_photo_list_from_vk(user_id):
        """Gets user photo from VK by user identification number:
        param user_id: user identification number
        return:
        photos_list: list of photos,
        photos_id_list: list of photos identification numbers
        """
        user = Person(user_id)
        photos_list = user.get_photos_of_person(user_id)
        photos_id_list = user.photo_id_list
        return photos_list, photos_id_list
