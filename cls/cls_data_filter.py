class DataFilter:

    def __init__(self, user_id):
        self.user_id = user_id

    def get_photo_list(self, raw_data: dict):
        ...