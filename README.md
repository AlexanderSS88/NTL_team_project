

### Командный проект по курсу «Профессиональная работа с Python»
### NTL_Dating
# VKinder

![log](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDefrJdZ0Rk1AV3OP6emi64uGbI-P0MB5bGg&usqp=CAU)

*[логотип взят из статьи](https://cpamonstro.com/smm/kak-sozdat-chat-bota-v-vk-bez-znaniya-koda/)* 


**VKinder**- *бот для поиска людей на платформе [VKontakte](https://vk.com/)* 

### Цель проекта

Разработать программу-бота для взаимодействия с базами данных социальной сети. 
Бот будет предлагать различные варианты людей для знакомств в социальной сети Вконтакте в виде диалога с пользователем.


## Начало работы
#### Програмное обеспечение
Для запуска программы нужен установленный Python версии не ниже 3.10

#### Токены

В целях защиты прав пользователей платформа приложений [Api VK](https://dev.vk.com) 
требует запуска требует использование ключей доступа- [токенов](#Tokens).   
Так же для работы бота с платформой требуются некоторые настройки приложения, 
описанные в блоке ["Данные для работы приложения"](#ApplicationData)
#### База данных
Для ускорения процесса списка аккаунтов VK для просмотра, используются внутренние ресурсы, 
такие как: 
* база данных 
* json файл *"db_in_json.json"*


## Использование

### При запуске 
программа предлагает простое <b name = "base_menu">меню</b>:

*Please choose the command:   
's'-scan VKontakte users to add to DataBase,  
'c' -get candidates list,     
'p' -get photos list, 
'b' -start bot,   
'q'- to quit:*

здесь соответсвенно:  
*'s'*- [получение данных о пользователях VK](#Scan),  
*'c'*- [получение списка пользователей](#choose),     
*'p'*- [получение списка фотографий потльзователя по его id](#photo), 
*'b'*- запуск бота,   
*'q'*- завершение программы

### <b name = "Scan">Сканирование</b>
Получение данных пользователей VK  
Программа просит ввести начальный и конечный номера id пользователей для получения данных.   

*Input start user id for scan:*  
и  
*Input last user id for scan:*

Note: *Спешим заметить, что текущее количество аккаутов на сайте превысило 72500000*  
Далее пользователю предлагается выбор возможности сохранениея данных в json файл:

*Should program write data to json file? (y/n):*

**По окончании** сканирования выводится [основное меню](#base_menu)

### <b name = "choose">Получение данных пользователя</b>
Здесь программа имитирует работу бота и ищет в **базе данных** список пользователей, 
отвечающих следующим параметрам, задавеамым пользователем:

минимальный возраст кандидата  
*Input min age of candidate:*	  
его максимальный возраст:  
*Input max age of candidate:*  
и город проживания:  
*Input the city name:*

**Результат** поиска выводится в виде списка идентификаторов пользователей VK

### <b name = "photo">Получение фотографий пользователя</b>
Программа запрашивает id потльзовате в VK:
*Input user id:*

Поиск произваодится в базе данных.  
**Результат** поиска выводится в виде списка идентификаторов пользователей VK

**Результат** поиска выводится в виде двух списков:  
* списка идентификаторов ыотографий  
* списка ссылок на фотографии в VK

## <b name = "Tokens">Токены</b>
#### [Токен пользователя можно получить по ссылке](https://oauth.vk.com/authorize?client_id=8116853&scope=wall,offline&redirect_uri=https://cosmio.io/api/vkinder/api.php&display=page&v=5.24&response_type=token)
#### Токены следует собрать в файле "tokens.txt" в формате:

    [TOKENS]
    vk_token = ваш токен для VK
    vk_bot_token = токен приложения
    [PASSWORDS]
    db_passw = пароль бады занных

## <b name = "ApplicationData">Данные для работы приложения</b>
#### содержатся в файле "application_data.ini":
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
    user_name = postgres
    port = 5432
    database_name = cours_w_DB
    host = localhost


### Выполнены задачи:
* Спроектирована база данных для программы
* Создано сообщество ВК https://vk.com/club214414105 c подключенным ботом
* Разработана программа-бота на Python с алгоритмом:
   1) Используя информацию (возраст, пол, город) о пользователе, который общается с ботом в ВК, производится поиск других людей (других пользователей ВК) для знакомств.****
   2) У тех людей, которые подошли под критерии поиска, получить три самые популярные фотографии в профиле. Популярность определяется по количеству лайков.
   3) Выводить в чат с ботом информацию о пользователе в формате: ФИО, Ссылка, Фото
   4) Реализовано меню "Следующий".
   5) Подгрузка пользователей осуществляется пакетами по N человек с записью в базу данных, когда данные в БД заканчиваются, осуществляется подгрузка следующих N пользователей Этот функционал позволяет обойти ограничение в поиске 1000 человек, так как используется смещение OFFSET и ограничение выборки COUNT
   6) Реализованы кнопки "Добавить в избранное" и "Показать избранные"
