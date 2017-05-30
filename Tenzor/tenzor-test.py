# -*- coding: UTF-8 -*-
"""Парсер статей с сайтов новостей.

Автор: Мартысюк Илья
E-Mail: martysyuk@gmail.com
т. +7-983-13-000-13
г. Новосибирск

Работа выполнена для компании Tenzor

Настройки тегов хранятся в файле config.py
"""

import config
import urllib.request
import sys
import re
import os


class ParseURL:
    """Класс обработки предоставленного URL
    URL передается параметром при объявлении класса.
    """

    def __init__(self, url):
        """Получение исходного кода страницы

        :param url: адрес обрабатываемой страницы.
        """
        try:
            response = urllib.request.urlopen(url)
            code = response.read()
        except urllib.error.HTTPError as error:
            exit('Ошибка открытия страницы {}'.format(error.code))
        self.content = code.decode(response.headers.get_content_charset())

    @staticmethod
    def replace_links(content):
        """Функция поиска и замены ссылок типа <a href="ССЫЛКА">ТЕКСТ</a> на тип ТЕКСТ [ССЫЛКА]

        :param content: Исходный текст для поиска и обработки ссылок
        :return: Текст с измененным типом ссылок
        """
        while True:
            try:
                content.index('<a href="')
                start_tag = content.find('<a href="')
                end_tag = content.find('>', start_tag) + 1
                start_url = start_tag + 9
                end_url = content.find('"', start_url+1)
                replace_point = content.find('</a>', end_url)
                link_url = str(content[start_url:end_url])
                content = content[:start_tag] + content[end_tag:replace_point] + ' [' + link_url + ']'\
                          + content[replace_point+4:]
            except ValueError:
                return content

    @staticmethod
    def cut_div_div(content):
        """Функция удаления кода между <div></div>

        :param content: Исходный текст для поиска и обработки <div></div>
        :return: Модифицированный текст
        """
        while True:
            open_tag = content.find('<div')
            close_tag = content[open_tag:].find('</div') + 6
            if open_tag != -1:
                content = content[:open_tag] + content[open_tag + close_tag:]
            else:
                return content

    def find_closed_div(self, point):
        """Функция поиска </div> в исходном блоке текста статьи

        :param point: Позиция в исходном тексте с которой начинать поиск закрыващего </div>
        :return: Позицию закрывающего </div>
        """
        div_count = 1
        while div_count > 0:
            point = self.content.find('<', point)
            check_text = self.content[point:point + 4]
            if check_text == '<div':
                div_count += 1
            elif check_text == '</di':
                div_count -= 1
            point += 1
        return point-1

    def parse(self, title_tag, text_tag):
        """Основная функция парсинга текста, обрабатывает исходный текст, находит заголовок и текст

        :param title_tag: Уникальный ключь блока заголовка статьи
        :param text_tag: Уникальный ключь блока текста статьи
        :return: Чистый текст с исправленнм типом ссылок и без излишнего HTML кода (не форматированный)
        """
        try:
            text_tag.index('image')
            tag_start = self.content.find(text_tag)
            start_point = self.content.find('src=', tag_start) + 5
            end_point = self.content.find('"', start_point)
            return str(self.content[start_point:end_point])
        except ValueError:
            tag_start = self.content.find(title_tag)
            start_point = self.content[tag_start:].find('>') + 1 + tag_start
            stop_point = self.content.find('<', start_point)
            text = self.content[start_point:stop_point] + '\n'*2

            tag_start = self.content.find(text_tag)
            start_point = self.content[tag_start:].find('>') + 1 + tag_start
            stop_point = self.find_closed_div(start_point)
            text = text + self.replace_links(self.cut_div_div(self.content[start_point:stop_point]))
            text = re.sub('</p>', '\n', text)
            text = re.sub(r'<[^>]*>', '', text)
            return text


def format_text(content, lenght_of_string=80):
    """Функци форматирования текста согласно заданию:
    1) Ширина строки не более 80 символов
    2) Перенос по словам

    :param content: Неформатированный текст
    :param lenght_of_string: Параметр указывающий максимальную ширину строки, по умолчанию = 80
    :return: Форматированный текст
    """
    paragraphs = content.split('\n')
    for index, paragraph in enumerate(paragraphs):
        point = lenght_of_string
        temp_list = []
        while point < len(paragraph):
            if paragraph[point-1:point] != ' ':
                cut_point = paragraph.rfind(' ', point-80, point) + 1
            else:
                cut_point = point
            temp_list.append(paragraph[:cut_point])
            paragraph = paragraph[cut_point:]
        if paragraph:
            temp_list.append(paragraph)
        if temp_list != '':
            paragraphs[index] = '\n'.join(temp_list)
    paragraphs = [value for value in paragraphs if value]
    return '\n\n'.join(paragraphs)


def save_to_txt_file(content, url):
    """ Функция сохраниения отформатированного текста в файл
    Преобразует полученный URL в пусть созранения файла и сохраняет результат в файл index.txt

    :param content: Форматированный и готовый для соранения текст
    :param url: Исходный адрес URL для преобразования его в путь сохранения файла
    """
    dir_name = os.path.realpath(os.path.dirname(sys.argv[0])) + '/' + re.split('\W+', url, 1)[1]
    file_name = os.path.join(dir_name, 'lenta-ru.txt')
    try:
        os.makedirs(dir_name)
    except OSError:
        pass
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)
        print('Обработка URL ({}) успешно завершена.'.format(url))
        print('Результат обработки сохранен в файл {}'.format(file_name))
    except FileNotFoundError:
        print('Ошибка сохранения файла')


def main():
    try:
        url = sys.argv[1]
    except IndexError:
        url = config.TEST_URL
    parser = ParseURL(url)
    save_to_txt_file(format_text(parser.parse(config.TITLE_TAG, config.TEXT_TAG)), url)

if __name__ == '__main__':
    main()
