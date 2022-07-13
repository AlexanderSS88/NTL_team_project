import configparser
import pathlib
from pathlib import Path


class VkData:

    def __init__(self, file_name="tokens/application_data.ini"):
        config = configparser.ConfigParser()  # create a parser object
        config.read(file_name)  # read confif file

        # [GROUP_DATA]
        self.GROUP_ID = config['GROUP_DATA']['group_id']
        # [API_DATA]
        self.API_VERSION = config['API_DATA']['api_version']
        self.APP_ID = config['API_DATA']['api_id']
        self.OWNER_ID = config['API_DATA']['owner_idp_token']

        # get token
        path = Path(pathlib.Path.cwd(), 'tokens', 'vk_bot_token.txt')
        with open(path, 'r') as t_file:
            self.token = t_file.read().strip()
