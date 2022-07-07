from pprint import pprint

from cls.cls_VkUrl import VkUrl

if __name__ == '__main__':
    vk = VkUrl('vk_token.txt')
    vk_id = '1'

    pprint(vk.get_personal_data(user_id=vk_id))
    pprint(vk.get_photo_f_profile(user_id=vk_id, album_name='wall'))
    pprint(vk.get_photo_f_profile(user_id=vk_id, album_name='profile'))
