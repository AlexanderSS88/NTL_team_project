class NewUser:

    def __init__(self, new_id):
        self.new_id = new_id
        self.dialog_status = 'new'
        self.candidates_data = {
            'candidates_data': {
                'min_age': 0,
                'max_age': 0,
                'city': ()
            }
        }
        self.candidates_list = []
        self.favorite_list = []
        self.current_candidate = 0

