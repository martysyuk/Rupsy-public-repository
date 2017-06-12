# -*- coding: UTF-8 -*-
"""Authon: Martysyuk Ilya
Title: Python Engineer
E-Mail: martysyuk@mail.ru
Phone: +7 (383) 299-1-373
Skype: martysyuk
"""

from urllib.parse import urlencode, urlparse
import requests
import time
from config import show_error


class VKApiRequest:

    def __init__(self, app_id, token_url='', scope='friends,messages,search,users,groups,wall', api_ver='5.64'):
        self.token = ''
        self.app_id = app_id
        self.api_ver = api_ver
        self.authorize_url = 'http://oauth.vk.com/authorize'
        auth_data = {
            'client_id': self.app_id,
            'display': 'popup',
            'response_type': 'token',
            'scope': scope,
            'v': self.api_ver
        }
        if token_url == '':
            token_url = '?'.join((self.authorize_url, urlencode(auth_data)))
            print('Перейдите по ссылке и скопируйте ее результат в переменную token_url:')
            print(token_url)
            exit(1)
        else:
            # token_url = 'https://oauth.vk.com/blank.html#access_token=775c71580676149067843d41ae6a34e2f48c5fc1f0a955e5f44e9106d18f90bde84407ff0ce3a334619e2&expires_in=86400&user_id=4119375'
            o = urlparse(token_url)
            fragments = dict((i.split('=') for i in o.fragment.split('&')))
            self.token = fragments['access_token']

    def get_user_id(self, user):
        return self.response('users.get', {'user_ids': user})[0]['id']

    @staticmethod
    def response_error(_response):
        if _response['error']['error_code'] == 6:
            time.sleep(0.5)
            return True
        else:
            if show_error:
                print('Error code: {}: {}'.format(_response['error']['error_code'], _response['error']['error_msg']))
            return False

    def response(self, _method, _params):
        _params.update({'access_token': self.token,
                        'v': self.api_ver
                        })
        while True:
            _response = requests.get('https://api.vk.com/method/' + _method, _params).json()
            try:
                return _response['response']
            except KeyError:
                if self.response_error(_response):
                    continue
                else:
                    return False


if __name__ == '__main__':
    pass