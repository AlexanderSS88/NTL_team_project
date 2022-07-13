import configparser  # импортируем библиотеку


class VkData:

    def __init__(self, file_name = "tokens/vk_config.txt"):
        config = configparser.ConfigParser()  # create a parser object
        config.read(file_name)  # read confif file

        # [GROUP_DATA]
        self.GROUP_ID = config['GROUP_DATA']['group_id']
        self.GROUP_TOKEN = config['GROUP_DATA']['group_token']
        # [API_DATA]
        self.API_VERSION = config['API_DATA']['api_version']
        self.APP_ID = config['API_DATA']['api_id']
        self.OWNER_ID = config['API_DATA']['owner_idp_token']
