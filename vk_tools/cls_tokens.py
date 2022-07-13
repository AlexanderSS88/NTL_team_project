import pathlib
from pathlib import Path
import configparser

from pprint import pprint


class Token:
    app_dict = {}

    def __init__(self):
        self.read_tokens()
        self.read_application_data()

    def read_tokens(self):
        pass

    def read_application_data(self):
        path = str(Path(pathlib.Path.cwd())) + '/tokens/application_data.ini'

        print(path)

        config = configparser.ConfigParser()
        config.read(path)

        pprint(config)

        self.app_dict.setdefault('APPLICATION', {
            'GROUP_ID': config['APPLICATION']['GROUP_ID'],
            'GROUP_TOKEN': config['APPLICATION']['GROUP_TOKEN'],
            'API_VERSION': config['APPLICATION']['API_VERSION'],
            'APPLICATION_TOKEN': config['APPLICATION']['APPLICATION_TOKEN'],
            'OWNER_ID': config['APPLICATION']['OWNER_ID']
        })
        self.app_dict.setdefault('GROUP_DATA', {'GROUP_ID': config['GROUP_DATA']['group_id']})
        # [API_DATA]

        self.app_dict.setdefault('API_DATA', {
            'API_VERSION': config['API_DATA']['API_VERSION'],
            'APP_ID': config['API_DATA']['APP_ID'],
            'OWNER_ID': config['API_DATA']['OWNER_ID']
        })

        self.app_dict.setdefault('DATABASE', {
            'user_name': config['DATABASE']['user_name'],
            'port': config['DATABASE']['port'],
            'database_name': config['DATABASE']['database_name'],
            'host': config['DATABASE']['host']
        })
