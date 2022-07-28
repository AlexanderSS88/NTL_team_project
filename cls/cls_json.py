import json

"""Class for interaction with json data storage file"""


class Add2Json:
    user_dict = {
        'id': str(),
        'candidates': [
            {'candidate_id': 0,
             'favorite': False}
        ]
    }

    def __init__(self, file_name):
        self.file_name = file_name

    def get_json_data(self):
        with open(self.file_name, encoding="utf-8", errors="ignore") as f:
            return json.load(f)

    def write_json(self, data_json: dict):
        try:
            with open(self.file_name, "w", encoding="utf-8") as f2:
                json.dump(data_json, f2, ensure_ascii=False, indent=3)
        except UnicodeDecodeError:
            print("Codec can't decode some byte. "
                  "Data wasn't recorded in json.")
        print('User data saved in json.')

    def add_new_user(self, user_id: str):
        data_json = self.get_json_data()

        if str(user_id) in data_json.keys():
            print('User is in json yet.')
        else:
            user_dict = self.user_dict
            user_dict['id'] = user_id
            data_json.update(user_dict)
            try:
                with open(self.file_name, "w", encoding="utf-8") as f2:
                    json.dump(data_json, f2, ensure_ascii=False, indent=3)
            except UnicodeDecodeError:
                print("Codec can't decode some byte. "
                      "Data wasn't recorded in json.")
            print('New User saved in json.')

        self.write_json(data_json)

    def add_candidate(self, user_id: str, candidate_id: str, in_favorites: bool):
        data_json = self.get_json_data()
        data_json[user_id]['candidates'].append({'candidate_id': candidate_id,
                                                 'favorite': in_favorites})
        self.write_json(data_json)

    def check_candidate(self, user_id, candidate_id):
        data_json = self.get_json_data()
        if str(user_id) in data_json.keys():
            for key, values in data_json:
                if key == user_id:
                    for candidate in values:
                        if candidate['candidate_id'] == candidate_id:
                            return True
                    break
        return False

# def add_2_json(self, user_id: str, user_dict: dict):
#     """Add user data to json storage file param:
#     user_id: user identification number
#     user_dict: dictionary with user data
#     """
#     user_json = {user_id: user_dict}
#     with open(self.file_name, encoding="utf-8", errors="ignore") as f:
#         second_json = json.load(f)
#     if str(user_id) in second_json.keys():
#         print('User is in json yet.')
#     else:
#         second_json.update(user_json)
#         try:
#             with open(self.file_name, "w", encoding="utf-8") as f2:
#                 json.dump(second_json, f2, ensure_ascii=False, indent=3)
#         except UnicodeDecodeError:
#             print("Codec can't decode some byte. "
#                   "Data wasn't recorded in json.")
#         print('User data saved in json.')
#
# def get_candidates_from_json(
#     self, min_age: int, max_age: int, city_name: str) -> list:
#     """Get list of candidates identification numbers from
#     json storage file by user age and user city param:
#     min_age:
#     max_age:
#     city_name:
#     return: list of candidates id
#     """
#     with open(self.file_name, encoding="utf-8", errors="ignore") as f:
#         data_json = json.load(f)
#         candidate_list = []
#     for user_id, user_data in data_json.items():
#         if min_age <= user_data['age'] <= max_age and user_data['city'] == city_name:
#             candidate_list.append(user_id)
#     return candidate_list
#
# def get_candidate_data_from_json(self, user_id):
#     """Get user data from json storage file param:
#     user_id: user identification number
#     return: data_json[str(user_id)]: dictionary with user data,
#     data_json[str(user_id)]['photos_id_list']: list of photos id of user
#     """
#     with open(self.file_name, encoding="utf-8", errors="ignore") as f:
#         data_json = json.load(f)
#     return data_json[str(user_id)], data_json[str(user_id)]['photos_id_list']
