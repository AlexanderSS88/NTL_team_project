import re
from random import randrange
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from cls.cls_Person import Person


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
    menu_1.add_callback_button(label='В избранное', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "add_to_favor"})
    menu_1.add_callback_button(label='Откртыть избранных', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "open_favor"})
    menu_1.add_line()
    menu_1.add_callback_button(label='Следующий', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "next"})
    menu_1.add_callback_button(label='Закончить', color=VkKeyboardColor.NEGATIVE,
                               payload={"type": "complete"})

    self.vk.messages.send(user_id=user_id, random_id=randrange(10 ** 7),
                          peer_id=user_id, keyboard=menu_1.get_keyboard(),
                          message=message)


def ask_user_after_favor(self, message, user_id='default'):
    if user_id == 'default':
        user_id = self.user_id
    settings = dict(one_time=False, inline=True)
    menu_1 = VkKeyboard(**settings)

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


def check_user_opinion_(self, message):
    if re.findall(self.pattern_favorite, message, flags=re.IGNORECASE):
        return 'add_to_favor'
    elif re.findall(self.pattern_end, message, flags=re.IGNORECASE):
        return 'complete'
    elif re.findall(self.pattern_next, message, flags=re.IGNORECASE):
        return 'next'
    else:
        return 'unknown'
