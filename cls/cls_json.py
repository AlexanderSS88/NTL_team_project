import json

"""Class for interaction with json data storage file"""


class Add2Json:

    def __init__(self, file_name):
        self.file_name = file_name

    def get_json_data(self) -> dict:
        """
        Read json data file
        :return: dictionary of data
        """
        with open(self.file_name, encoding="utf-8", errors="ignore") as f:
            return json.load(f)

    def write_json(self, data_json: dict):
        """
        Rewrite json file with new data
        :param data_json:
        :return: None
        """
        try:
            with open(self.file_name, "w", encoding="utf-8") as f2:
                json.dump(data_json, f2, ensure_ascii=False, indent=3)
        except UnicodeDecodeError:
            print("Codec can't decode some byte. "
                  "Data wasn't recorded in json.")
        print('User data saved in json.')

    def add_new_user(self, user_id: str):
        """
        Add a new client to json file
        :param user_id:
        :return: None
        """
        data_json = self.get_json_data()

        if str(user_id) in data_json.keys():
            print('User is in json yet.')
        else:
            user_dict = {user_id: [{'candidate_id': 0,
                                    'favorite': False}]
                         }
            data_json.update(user_dict)
            try:
                with open(self.file_name, "w", encoding="utf-8") as f2:
                    json.dump(data_json, f2, ensure_ascii=False, indent=3)
            except UnicodeDecodeError:
                print("Codec can't decode some byte. "
                      "Data wasn't recorded in json.")
            print('New User saved in json.')

    def add_candidate(self, user_id: str, candidate_id: int, in_favorites: bool):
        """
        Add a new candidate for client
        :param user_id:
        :param candidate_id:
        :param in_favorites:
        :return: None
        """
        data_json = self.get_json_data()
        data_json[str(user_id)].append({'candidate_id': candidate_id,
                                        'favorite': in_favorites})
        self.write_json(data_json)

    def check_candidate(self, user_id: int, candidate_id: int):
        """
        Check if candidate was presented to client yet
        :param user_id:
        :param candidate_id:
        :return: False or True up to check result
        """
        data_json = self.get_json_data()
        if str(user_id) in data_json.keys():
            for item in data_json[str(user_id)]:
                if item['candidate_id'] == candidate_id:
                    return True
        return False
