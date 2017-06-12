# -*- coding: UTF-8 -*-
"""Authon: Martysyuk Ilya
Title: Python Engineer
E-Mail: martysyuk@mail.ru
Phone: +7 (383) 299-1-373
Skype: martysyuk

Доработать:
1) Проверку сделаных репостов, чтобы не повторялись.
2) сделать автоматическую авторизацию уазанного пользователя
"""

import vk_api
import time
import pandas as pd
import json


class Main:
    def __init__(self):
        print('Starting searching posts...')

        self.cfg_file_name = 'config.json'
        self.posted_file_name = 'posted.json'

        self.cfg = self.load_json(self.cfg_file_name)
        self.posted = self.load_json(self.posted_file_name)

        self.vk = vk_api.VKAuth(self.cfg['api']['scope'],
                                self.cfg['api']['app_id'],
                                self.cfg['api']['api_ver'],
                                self.cfg['api']['login'],
                                self.cfg['api']['password'])
        self.vk.auth()
        self.df = pd.DataFrame(columns=['owner_id', 'post_id', 'likes'])
        self.interests = self.cfg['search']['interests']
        self.groups_with_interests = dict()
        self.date = time.localtime()
        self.post_to_repost = list()
        self.already_posted = list()
        self.groups_list = list()

        self.get_groups_list()
        self.load_posts_from_groups()
        self.do_repost()

    @staticmethod
    def load_json(_file_name):
        try:
            with open(_file_name, 'r', encoding='UTF8') as _file:
                return json.load(_file)
        except FileNotFoundError:
            exit('File {} not found! Program exit...'.format(_file_name))

    @staticmethod
    def save_json(_data, _file_name):
        try:
            with open(_file_name, 'w', encoding='UTF8') as _file:
                json.dump(_data, _file, sort_keys=True, ensure_ascii=False, indent=2)
        except IOError:
            print('Ошибка записи файла {}'.format(_file_name))

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
        query = {'count': 30,
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

    def do_repost(self):
        for each in range(len(self.df)):
            _getter = self.df.iloc[each]
            _post_id = 'wall{}_{}'.format(_getter['owner_id'], _getter['post_id'])
            if _post_id not in self.posted:
                print('Делаем репост записи: {}'.format(_post_id))
                self.vk.get_response('wall.repost', {'object': _post_id,
                                                     'group_id': self.cfg['repost']['repost_to'],
                                                     'message': self.cfg['repost']['add_tags']})
                self.posted.append(_post_id)
                self.increase_counter()
                self.save_json(self.posted, self.posted_file_name)
                self.save_json(self.cfg, self.cfg_file_name)
                print('Запись опубликованна.')
                exit(0)
            else:
                print('В данной группе новых постов нет. Переключаемся на следующий интерес.')
                self.increase_counter()
                self.save_json(self.cfg, self.cfg_file_name)
                self.get_groups_list()
                self.load_posts_from_groups()
                self.do_repost()

if __name__ == '__main__':
    wrapper = Main()
