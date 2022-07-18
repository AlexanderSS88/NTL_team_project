import json
from pprint import pprint

class Add2Json():

    def __init__(self, file_name):
        self.file_name = file_name
        # json_base = {}
        # with open(self.file_name, "w") as f:
        #     json.dump(json_base, f, ensure_ascii=False, indent=3)

    def add_2_json(self, user_id: str, user_dict: dict):
        user_json = {user_id: user_dict}

        print('\nuser_dict:')
        pprint(user_dict)

        second_json = {}

        with open(self.file_name) as f:
            second_json = json.load(f)
            print('\nsecond_json1:')
            pprint(second_json)

        if str(user_id) in second_json.keys():
            print('User is in json yet.')

        else:
            second_json.update(user_json)

            print('\nsecond_json2:')
            pprint(second_json)

            with open(self.file_name, "w") as f2:
                json.dump(second_json, f2, ensure_ascii=False, indent=3)

            print('User data saved in json.')