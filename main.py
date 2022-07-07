from pprint import pprint

from cls.cls_VkUrl import VkUrl

if __name__ == '__main__':
    vk = VkUrl('vk_token.txt')
    vk_id = '84482680'

    pprint(vk.get_personal_data(user_id=vk_id))

    album_list = ['wall', 'profile']
    album_list.extend(vk.search_albums(user_id=vk_id))
    pprint(album_list)
    pprint(vk.get_photo_f_profile(user_id=vk_id, album_name_list=album_list))
