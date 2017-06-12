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

    def __init__(self, _file_name):
        print('Starting searching posts...')

        try:
            with open(_file_name, 'r', encoding='UTF8') as cfg_file:
                self.cfg = json.load(cfg_file)
        except FileNotFoundError:
            exit('Configuration file not found! Program exit...')

        self.vk = vk_api.VKAuth(self.cfg['api']['scope'],
                                self.cfg['api']['app_id'],
                                self.cfg['api']['api_ver'],
                                self.cfg['api']['login'],
                                self.cfg['api']['password'])
        self.vk.auth()

        self.df = pd.DataFrame(columns=['owner_id', 'post_id', 'likes'])

        self.interests = self.cfg['search']['interests']
        self.groups_with_interests = dict()
        self.now_time = time.time()
        self.maximum_old_posts_time = self.now_time - 60 * 60 * 24
        self.post_to_repost = list()
        self.already_posted = list()

    def get_groups_by_interests(self):
        query = {'type': 'group',
                 'country_id': 1,
                 'sort': 2,
                 'count': self.cfg['search']['maximum_checking_count']}
        groups_list = []
        for interest in self.interests:
            query.update({'q': interest})
            response = self.vk.get_response('groups.search', query)
            for each in response['items']:
                groups_list.append('-'+str(each['id']))
            self.groups_with_interests.update({interest: groups_list})
            groups_list = []

    def search_posts_with_max_likes(self):
        query = {'count': self.cfg['search']['maximum_checking_count'],
                 'filter': 'owner'}
        for each in self.groups_with_interests:
            for group_id in self.groups_with_interests[each]:
                query.update({'owner_id': group_id})
                _response = self.vk.get_response('wall.get', query)
                try:
                    for post in _response['items']:
                        if post['date'] > self.maximum_old_posts_time:
                            self.df.loc[len(self.df)] = [post['owner_id'], post['id'], post['likes']['count']]
                except TypeError:
                    pass
            self.df = self.df.sort_values('likes', ascending=0).head(self.cfg['repost']['reposts_count'])
            self.repost()
            self.df = pd.DataFrame(columns=['owner_id', 'post_id', 'likes'])
            if self.cfg['repost']['repost_wait'] > 0:
                print('Waiting {} seconds to next repost...'.format(self.cfg['repost']['repost_wait']))
                time.sleep(self.cfg['repost']['repost_wait'])

    def repost(self):
        for each in range(len(self.df)):
            _getter = self.df.iloc[each]
            self.post_to_repost.append('wall{}_{}'.format(str(_getter['owner_id']).replace('.0', ''),
                                                          str(_getter['post_id'])).replace('.0', ''))
        for each in self.post_to_repost:
            if each not in self.already_posted:
                self.vk.get_response('wall.repost', {'object': each,
                                                     'group_id': self.cfg['repost']['repost_to'],
                                                     'message': self.cfg['repost']['add_tags']})
                self.already_posted.append(each)
                print('Repost done!')


if __name__ == '__main__':
    wrapper = Main('vkar.json')
    wrapper.get_groups_by_interests()
    wrapper.search_posts_with_max_likes()
