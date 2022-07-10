import json
import re
import csv
from vk_api import VkApi
from random import randrange
from cls.cls_Person import Person
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_tools.cls_read_config import VkData

# person = ......
# Данные в формате:
# Имя Фамилия
# ссылка на профиль
# три фотографии в виде attachment(https://dev.vk.com/method/messages.send)


person = Person('1')  # потом разберёмся
vk_cfg = VkData('vk_config.txt')

CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')

vk_session = VkApi(token=vk_cfg.GROUP_TOKEN, api_version=vk_cfg.API_VERSION)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=vk_cfg.GROUP_ID)

settings = dict(one_time=False, inline=True)
menu_1 = VkKeyboard(**settings)
menu_1.add_callback_button(label='В избранное', color=VkKeyboardColor.POSITIVE, payload={"type": "add_to_favor"})
menu_1.add_line()
menu_1.add_callback_button(label='В чёрный список', color=VkKeyboardColor.NEGATIVE,
                           payload={"type": "add_to_blacklist"})
menu_1.add_line()
menu_1.add_callback_button(label='Следующий', color=VkKeyboardColor.PRIMARY, payload={"type": "next"})
menu_1.add_line()
menu_1.add_callback_button(label='Откртыть избранных', color=VkKeyboardColor.PRIMARY, payload={"type": "open_favor"})
menu_1.add_line()

menu_2 = VkKeyboard(**settings)
menu_2.add_callback_button(label='Сочный лайк', color=VkKeyboardColor.POSITIVE, payload={"type": "like"})
menu_2.add_line()
menu_2.add_callback_button(label='Отменить лайк', color=VkKeyboardColor.NEGATIVE, payload={"type": "return_like"})
menu_2.add_line()


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})


for event in longpoll.listen():
    write_msg(event.user_id,
              f"Привет, {event.user_id}! Предлагаю тебе попробовать познакомиться с кем-нибудь. Согласен? :)")
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            pattern_yes = "(давай)|(да)|(ок)|(хорош)|(соглас)|(добро)|(ладно)"
            pattern_no = "(нет)|(не)|(против)|(пока)|(досвидан)|(доброго)|(бай)"
            if re.findall(pattern_yes, request, flags=re.IGNORECASE):
                write_msg(event.user_id, person)

                # добавляем в избранное
                if event.object.payload.get('type') == 'add_to_favor':
                    ...
                # в чёрный список
                elif event.object.payload.get('type') == 'add_to_blacklist':
                    ...
                # следующий
                elif event.object.payload.get('type') == 'next':
                    ...

                # открываем список избранных
                elif event.object.payload.get('type') == 'open_favor':
                    ...

            elif re.findall(pattern_no, request, flags=re.IGNORECASE):
                write_msg(event.user_id, "Скатертью дорога!!!")
            else:
                write_msg(event.user_id, "Не понял вашего ответа... Повтори!")

    # if event.object.payload.get('type') == 'like':
    #     vk.likes.add{'type': photo, 'owner_id': owner_hoto_id, 'item_id'= item_id}
    # elif event.object.payload.get('type') == 'return_like':
    #     vk.likes.delete{'type': photo, 'owner_id': owner_hoto_id, 'item_id' = item_id}
