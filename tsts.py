from cls.cls_json import Add2Json

add_jeson = Add2Json('db_in_json.json')

print(add_jeson.get_candidates_from_json(min_age= 30, max_age=35, city_name= 'Москва'))

user_data, photo_list = add_jeson.get_candidate_data_from_json(2321)

print(f'user_data: {user_data}')
print(f'photo_list: {photo_list}')
print(f"{user_data['first_name']} " \
                   f"{user_data['last_name']}" \
                   f"\n{user_data['url']}")