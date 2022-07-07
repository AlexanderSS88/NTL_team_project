class HttpR:
    def __init__(self, token_file_n: str):
        """
        Here program takes the TOKEN
        """

        # to take a token from file
        with open(token_file_n, 'r') as t_file:
            self.token = t_file.read().strip()
            print(self.token)
