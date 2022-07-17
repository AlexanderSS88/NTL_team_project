from cls.cls_person_list_iteration import PersonListStack

class ClsClient:
    dialog_status = str
    candidates_list = PersonListStack([])
    candidates_data = {'min_age': 0,
                       'max_age': 0,
                       'city': ''}

    def __init__(self, client_id):
        self.client_id = client_id

