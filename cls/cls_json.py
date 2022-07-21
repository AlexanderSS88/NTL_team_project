import json

"""
Class for interaction with json data storage file
"""
class Add2Json:

    def __init__(self, file_name):
        self.file_name = file_name

    def add_2_json(self, user_id: str, user_dict: dict):
        """
        Add user data to json storage file
        :param user_id: user identification number
        :param user_dict: dictionary with user data
        """
        user_json = {user_id: user_dict}

        second_json = {}

        with open(self.file_name, encoding="utf-8", errors="ignore") as f:
            second_json = json.load(f)

        if str(user_id) in second_json.keys():
            print('User is in json yet.')

        else:
            second_json.update(user_json)

            try:
                with open(self.file_name, "w", encoding="utf-8") as f2:
                    json.dump(second_json, f2, ensure_ascii=False, indent=3)
            except UnicodeDecodeError:
                print("Codec can't decode some byte. Data wasn't recorded in json.")

            print('User data saved in json.')

    def get_candidates_from_json(self, min_age: int, max_age: int, city_name: str) -> list:
        """
        Get list of candidates identification numbers from json storage file by user age and user city
        :param min_age:
        :param max_age:
        :param city_name:
        :return: list of candidates id
        """

        with open(self.file_name, encoding="utf-8", errors="ignore") as f:
            data_json = json.load(f)

            candidate_list = []

        for user_id, user_data in data_json.items():
            if min_age <= user_data['age'] <= max_age and user_data['city'] == city_name:
                candidate_list.append(user_id)

        return candidate_list

    def get_candidate_data_fron_json(self, user_id):
        """
        Get user data from json storage file
        :param user_id: user identification number
        :return: data_json[str(user_id)]: dictionary with user data,
                 data_json[str(user_id)]['photos_id_list']: list of photos id of user
        """
        with open(self.file_name, encoding="utf-8", errors="ignore") as f:
            data_json = json.load(f)

        return data_json[str(user_id)], data_json[str(user_id)]['photos_id_list']
