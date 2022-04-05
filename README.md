# telelogger_flask

Для работы необходимо в корне проекта создать файл .env
В него разместить к ключа:
TELEGRAM_TOKEN 
AUTH_STRING

....

Структура запроса JSON

{
    "recipients": [""], 
    "msg": [ 
        {"type": "header", "text": "Hello World"},
        {"type": "pre", "text": "print(001011)\nprint(001011)\nprint(001011)\nprint(001011)"},
        {"type": "footer", "text": "Описание сообщения"}
    ],
    "auth": ""
}

recipients - содержит список строк получаетелей сообщений
msg - Список словарей с ключами type и text
auth - авторизационная строка
