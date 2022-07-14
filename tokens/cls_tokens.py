import pathlib
from pathlib import Path
import configparser


class Token:
    app_dict = {}

    def __init__(self, direct_name='tokens'):
        self.direct_name = direct_name
        self.read_tokens()
        self.read_application_data()

    def read_tokens(self):
        path = str(Path(pathlib.Path.cwd())) + '/' + self.direct_name + '/tokens.txt'

        config = configparser.ConfigParser()
        config.read(path)

        self.app_dict.setdefault('TOKENS', {
            'vk_token': config['TOKENS']['vk_token'],
            'vk_bot_token': config['TOKENS']['vk_bot_token']
        })
        self.app_dict.setdefault('PASSWORDS', {
            'db_passw': config['PASSWORDS']['db_passw']
        })
        self.app_dict.setdefault('APPLICATION_TOKENS', {
            'GROUP_TOKEN': config['APPLICATION_TOKENS']['GROUP_TOKEN'],
            'APPLICATION_TOKEN': config['APPLICATION_TOKENS']['APPLICATION_TOKEN']
        })

    def read_application_data(self):
        path = str(Path(pathlib.Path.cwd())) + '/' + self.direct_name + '/application_data.ini'

        config = configparser.ConfigParser()
        config.read(path)

        self.app_dict.setdefault('APPLICATION', {
            'GROUP_ID': config['APPLICATION']['GROUP_ID'],
            # 'GROUP_TOKEN': config['APPLICATION']['GROUP_TOKEN'],
            'API_VERSION': config['APPLICATION']['API_VERSION'],
            # 'APPLICATION_TOKEN': config['APPLICATION']['APPLICATION_TOKEN'],
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
