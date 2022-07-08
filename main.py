from pprint import pprint

from cls.cls_VkUrl import VkUrl

if __name__ == '__main__':
    vk = VkUrl('vk_token.txt')
    vk_ = VkUrl('vk_token_.txt')
    vk_id = '668524'

    pprint(vk.get_personal_data(user_id=vk_id))

    album_list = ['wall', 'profile']
    album_list.extend(vk_.search_albums(user_id=vk_id))
    pprint(album_list)
    pprint(vk.get_photo_f_profile(user_id=vk_id, album_name_list=album_list))
