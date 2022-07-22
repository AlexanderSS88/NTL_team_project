This is the folder for your tokens.

Токены следует собрать в файле "tokens.txt" в формате:
    [TOKENS]
    vk_token = токен Вконтакте
    vk_bot_token = токен приложения
    [PASSWORDS]
    db_passw = пароль для базы данных

Основные данные для работы приложения содержатся в файле "application_data.ini":
    [APPLICATION]
    GROUP_ID = 214414105
    API_VERSION = 5.131
    APP_ID = 8213519
    OWNER_ID = 571567527
    CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')
    [GROUP_DATA]
    GROUP_ID='214414105'
    [API_DATA]
    API_VERSION='5.131'
    APP_ID='8213519'
    OWNER_ID='571567527'
    [DATABASE]
    user_name = postgres: имя пользователя базы данных
    port = 5432: порт, данное значение присваивается по-умолчению
    database_name = cours_w_DB: имя вашей базы данных
    host = localhost- для локальной базы

