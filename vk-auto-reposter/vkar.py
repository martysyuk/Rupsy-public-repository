# -*- coding: UTF-8 -*-
"""Authon: Martysyuk Ilya
Title: Python Engineer
E-Mail: martysyuk@mail.ru
Phone: +7 (383) 299-1-373
Skype: martysyuk

Доработать:
- Шифрование  пароля,  чтобы  не  хранить  его  в  открытом виде в файле
- Убрать авторизацию при каждом запуске программы
- Добавить  получение  и  запись TOKEN в файл конфигурации, если прежний
TOKEN не был найден или оказался не действующим
"""

import vk_api
import time
import pandas as pd
import json
import os


class Main:
    def __init__(self):

        self.__version__ = '1.3.1'

        print('VKar v.{} - VKontakte auto reposter\n'
              '---------------------------------------------------------\n'
              'Программа автоматического поиска публикаций по  интересам\n'
              'с наибольшим количеством лайков и автоматическим репостом\n'
              'этих записей на стену Вашего сообщества.\n\n'
              'Автор: Мартысюк Илья\n'
              'E-Mail: martysyuk@gmail.com\n'.format(self.__version__))

        _cfg_file_path = os.path.dirname(os.path.realpath(__file__))
        self.cfg_file_name = os.path.join(_cfg_file_path, 'config.json')
        self.posted_file_name = os.path.join(_cfg_file_path, 'posted.json')

        self.cfg = self.load_json(self.cfg_file_name)
        self.posted = self.load_json(self.posted_file_name)

        self.vk = vk_api.VKAuth(self.cfg['api']['scope'],
                                self.cfg['api']['app_id'],
                                self.cfg['api']['api_ver'],
                                self.cfg['api']['login'],
                                self.cfg['api']['password'],
                                show_error=self.cfg['show_errors'])
        self.vk.auth()
        self.df = pd.DataFrame(columns=['owner_id', 'post_id', 'likes'])
        self.interests = self.cfg['search']['interests']
        self.groups_with_interests = dict()
        self.today = time.strftime("%Y%m%d")
        self.date = time.localtime()
        self.post_to_repost = list()
        self.already_posted = list()
        self.groups_list = list()
        self.try_couter = 0

        self.get_groups_list()
        self.load_posts_from_groups()
        self.do_repost()

    @staticmethod
    def load_json(_file_name):
        try:
            with open(_file_name, 'r', encoding='UTF8') as _file:
                return json.load(_file)
        except FileNotFoundError:
            exit('Ошибка: файл {} не найден.'.format(_file_name))

    @staticmethod
    def save_json(_data, _file_name):
        try:
            with open(_file_name, 'w', encoding='UTF8') as _file:
                json.dump(_data, _file, sort_keys=True, ensure_ascii=False, indent=2)
        except IOError:
            exit('Ошибка записи файла {}'.format(_file_name))

    def get_groups_list(self):
        try:
            _interest = self.cfg['search']['interests'][self.cfg['search']['checking_interest']]
            if _interest:
                query = {'type': 'group',
                         'country_id': 1,
                         'sort': 2,
                         'count': self.cfg['search']['maximum_groups_in_list'],
                         'q': _interest}
                _response = self.vk.get_response('groups.search', query)
                for each in _response['items']:
                    if (each['is_closed'] == 0) & (str(each['id']) not in self.cfg['search']['ignored_groups']):
                        self.groups_list.append('-' + str(each['id']))
            else:
                exit('В файле настроек не указан ни один интерес.')
        except IndexError:
            print('Ошибка конфигурационного файла. Не соответсвие количесва интересов проверяемому индексу.')

    def load_posts_from_groups(self):
        query = {'count': self.cfg['search']['maximum_posts_in_list'],
                 'filter': 'owner'}
        for group_id in self.groups_list:
            query.update({'owner_id': group_id})
            _response = self.vk.get_response('wall.get', query)
            try:
                for post in _response['items']:
                    if time.gmtime(post['date'])[2] == self.date[2] - 2:
                        self.df.loc[len(self.df)] = [str(post['owner_id']).replace('.0', ''),
                                                     str(post['id']).replace('.0', ''),
                                                     post['likes']['count']]
            except TypeError:
                pass
        self.df = self.df.sort_values('likes', ascending=False)

    def increase_counter(self):
        if self.cfg['search']['checking_interest'] < (len(self.cfg['search']['interests']) - 1):
            self.cfg['search']['checking_interest'] += 1
        else:
            self.cfg['search']['checking_interest'] = 0

    def get_post_data(self, _post_id):
        _attach_list = list()
        _response = self.vk.get_response('wall.getById', {'posts': _post_id})[0]
        try:
            for each in _response['attachments']:
                _attach_list.append('{}{}_{}'.format(each['type'], each[each['type']]['owner_id'],
                                                     each[each['type']]['id']))
            _attach = ','.join(_attach_list)
        except KeyError:
            _attach = ''
        return _response['text'], _attach, str(_response['owner_id'])

    def do_repost(self):
        try:
            _posted = self.posted[self.today]
        except KeyError:
            _posted = list()
        for each in range(len(self.df)):
            _getter = self.df.iloc[each]
            _post_id = '{}_{}'.format(_getter['owner_id'], _getter['post_id'])
            if _post_id not in _posted:
                _text, _attach, _owner = self.get_post_data(_post_id)
                _message = '{}\n\n{}\n\n[[club{}|Автор публикации]]'.format(_text, self.cfg['repost']['add_tags'],
                                                                            _owner.replace('-', ''))
                _query = {'owner_id': '-' + self.cfg['repost']['repost_to'],
                          'from_group': 1,
                          'message': _message}
                if _attach:
                    _query.update({'attachments': _attach})
                self.vk.get_response('wall.post', _query)
                _posted.append(_post_id)
                self.posted = {self.today: _posted}
                self.increase_counter()
                self.save_json(self.posted, self.posted_file_name)
                self.save_json(self.cfg, self.cfg_file_name)
                print('Запись опубликованна.')
                exit(0)
        if self.try_couter < len(self.cfg['search']['interests']) - 1:
            self.try_couter += 1
            print('В данной группе новых постов нет. Переключаемся на следующий интерес.')
            self.increase_counter()
            self.save_json(self.cfg, self.cfg_file_name)
            self.get_groups_list()
            self.load_posts_from_groups()
            self.do_repost()
        else:
            exit('На сегодня свежих постов больше нет!')


if __name__ == '__main__':
    wrapper = Main()
