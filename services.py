import copy
from abc import ABC

import requests as requests
from flask import request

from dotenv import dotenv_values


class Messenger(ABC):

    def send_message(self, messages):
        pass


class Telegram(Messenger):

    def __init__(self, token):
        self.uri = f'https://api.telegram.org/bot{token}/sendMessage'

    def send_message(self, messages):
        result = []
        for message in messages:
            r = requests.post(url=self.uri, json=message)
            if r.status_code == 200:
                result.append({'error': None, 'message': 'Messages was successfully sent!'})
            else:
                result.append({'error': True, 'message': 'Сообщение содежржит ошибку и не может быть отправлено!'})
        return result

    @staticmethod
    def create():
        return HandlerFactory.create_telegram()


class Viber(Messenger):

    def send_message(self, messages):
        raise NotImplemented('Implemented later')

    @staticmethod
    def create():
        return HandlerFactory.create_viber()


class HandlerFactory:

    @staticmethod
    def _new_handler(messanger, auth_string):
        return HandlerMsg(messanger=messanger, auth=auth_string)

    @staticmethod
    def create_telegram():
        env = Utils.load_env()
        token = env.get('TELEGRAM_TOKEN')
        auth_string = env.get('AUTH_STRING')
        messanger = Telegram(token)
        return HandlerFactory._new_handler(messanger, auth_string)

    @staticmethod
    def create_viber():
        env = Utils.load_env()
        auth_string = env.get('AUTH_STRING')
        messanger = Viber()
        return HandlerFactory._new_handler(messanger, auth_string)


class HandlerMsg:
    def __init__(self, messanger, auth):
        self.messenger = messanger
        self.auth = auth  # string authorization

    @property
    def prepared_messages(self):
        incoming_data = Utils.parser_json()
        Utils.auth(self.auth, incoming_data)
        messages = []
        for recipient in incoming_data['recipients']:
            message = Utils.get_structure_msg()
            message['chat_id'] = recipient
            text_msg = ''
            for part in incoming_data['msg']:
                text_msg = text_msg + BuilderMsg.build_msg(part['type'], part['text'])
            message['text'] = text_msg
            messages.append(message)
        return messages

    def send_message(self):
        messages = self.prepared_messages
        return self.messenger.send_message(messages)


class Utils:

    @staticmethod
    def auth(auth_string, messages):
        if auth_string != messages['auth']:
            raise Exception("Invalid request")

    @staticmethod
    def parser_json(data=None):
        if data is None:
            return request.json

    @staticmethod
    def load_env():
        return dotenv_values('.env')

    @staticmethod
    def get_structure_msg():
        return {
            'chat_id': '',
            'text': '',
            'disable_web_page_preview': False,
            'disable_notification': False,
            'parse_mode': 'HTML'
        }


class BuilderMsg:

    tables_code = {
        'header': ['<b>', None, '</b>', '\n\n'],
        'code': ['<code>', None, '</code>', '\n'],
        'pre': ['<pre language="python">', None, '</pre>', '\n'],
        'footer': ['-'*20+'\n', None, '\n']
    }

    @classmethod
    def build_msg(cls, key, value):
        if cls.tables_code.get(key) is None:
            raise Exception('unknown msg!')
        part_message = copy.deepcopy(cls.tables_code)
        part_message[key][1] = value
        return ''.join(part_message[key])
