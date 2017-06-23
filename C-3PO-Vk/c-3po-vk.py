# -*- coding: UTF-8 -*-
"""Authon: Martysyuk Ilya
Title: Python Engineer
E-Mail: martysyuk@mail.ru
Phone: +7 (383) 299-1-373
Skype: martysyuk"""

import json
import os
import time

import pandas as pd
import vk_api


class Main:
    def __init__(self):

        self.done = False

        self.cfg = cfg
        self.posted = posted
        self.cfg_file_name = cfg_file_path
        self.posted_file_name = posted_file_path

        self.vk = vk_api.VKAuth(self.cfg['api']['scope'],
                                self.cfg['api']['app_id'],
                                self.cfg['api']['api_ver'],
                                self.cfg['api']['login'],
                                self.cfg['api']['password'],
                                show_error=self.cfg['show_errors'])
        self.vk.auth()

        self.today = time.strftime("%Y%m%d")
        self.df = pd.DataFrame(columns=['owner_id', 'post_id', 'likes'])

    def __call__(self, repost_to):
        self.repost_to = repost_to
        self.interests = self.cfg['groups'][repost_to]['interests']
        self.df = pd.DataFrame(columns=['owner_id', 'post_id', 'likes'])
        self.date = time.localtime()
        self.groups_with_interests = dict()
        self.post_to_repost = list()
        self.already_posted = list()
        self.groups_list = list()
        self.try_couter = 0

        print('Начинаем поиск постов для сообщества {} по интересам: {}'.format(self.repost_to, self.interests))

        self.get_groups_list()
        self.load_posts_from_groups()
        self.do_repost()

    @staticmethod
    def save_json(_data, _file_name):
        try:
            with open(_file_name, 'w', encoding='UTF8') as _file:
                json.dump(_data, _file, sort_keys=True, ensure_ascii=False, indent=2)
        except IOError:
            exit('Ошибка записи файла {}'.format(_file_name))

    def get_groups_list(self):
        try:
            _interest = self.interests
            if _interest:
                query = {'type': 'group',
                         'country_id': 1,
                         'sort': 2,
                         'count': self.cfg['groups'][self.repost_to]['maximum_groups_in_list'],
                         'q': _interest}
                _response = self.vk.get_response('groups.search', query)
                for each in _response['items']:
                    if (each['is_closed'] == 0) & (
                                str(each['id']) not in self.cfg['groups'][self.repost_to]['ignored_groups']):
                        self.groups_list.append('-' + str(each['id']))
            else:
                exit('В файле настроек не указан ни один интерес.')
        except IndexError:
            print('Ошибка конфигурационного файла. Не соответсвие количесва интересов проверяемому индексу.')

    def load_posts_from_groups(self):
        query = {'count': self.cfg['groups'][self.repost_to]['maximum_posts_in_list'],
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
        if self.cfg['groups'][self.repost_to]['checking_interest'] < (
                    len(self.cfg['groups'][self.repost_to]['interests']) - 1):
            self.cfg['groups'][self.repost_to]['checking_interest'] += 1
        else:
            self.cfg['groups'][self.repost_to]['checking_interest'] = 0

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
        try:
            _history_lenght = len(_response['copy_history']) - 1
            return _response['copy_history'][_history_lenght]['text'], _attach, str(
                _response['copy_history'][_history_lenght]['owner_id'])
        except KeyError:
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
                print('Делаем репост записи {} в сообщество {}.'.format(_post_id, self.repost_to))
                _text, _attach, _owner = self.get_post_data(_post_id)
                _message = '{}\n\n{}'.format(_text, self.cfg['groups'][self.repost_to][
                    'repost_tags'])
                if self.cfg['groups'][self.repost_to]['copyright']:
                    _message = '{}\n\nИсточник публикации: @club{}'.format(_message, _owner.replace('-', ''))
                _query = {'owner_id': '-' + self.repost_to,
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
                print('Запись в сообществе опубликованна.\n'.format(self.repost_to))
                self.done = True
                break
        if (self.try_couter < len(self.cfg['groups'][self.repost_to]['interests']) - 1) and (self.done is False):
            self.try_couter += 1
            print('В данной группе новых постов нет. Переключаемся на следующий интерес.')
            self.increase_counter()
            self.save_json(self.cfg, self.cfg_file_name)
            self.get_groups_list()
            self.load_posts_from_groups()
            self.do_repost()


def load_json(_file_name):
    try:
        with open(_file_name, 'r', encoding='UTF8') as _file:
            return json.load(_file)
    except FileNotFoundError:
        exit('Ошибка: файл {} не найден.'.format(_file_name))
    except json.decoder.JSONDecodeError:
        exit('Ошибка в формате файла JSON: {}'.format(_file_name))


if __name__ == '__main__':
    __version__ = '1.4.0'

    print('C-3PO-vk v.{} - VKontakte auto reposter\n'
          '---------------------------------------------------------\n'
          'Программа автоматического поиска публикаций по  интересам\n'
          'с наибольшим количеством лайков и автоматическим репостом\n'
          'этих записей на стену Вашего сообщества.\n\n'
          'Автор: Мартысюк Илья\n'
          'E-Mail: martysyuk@gmail.com\n'.format(__version__))

    app_dir = os.path.dirname(os.path.realpath(__file__))
    cfg_file_path = os.path.join(app_dir, 'config.json')
    posted_file_path = os.path.join(app_dir, 'posted.json')
    cfg = load_json(cfg_file_path)
    posted = load_json(posted_file_path)
    methods = list()

    repost = Main()

    for repost_to_id in cfg['groups']:
        if cfg['groups'][repost_to_id]['active']:
            repost(repost_to_id)
