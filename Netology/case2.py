# -*- coding: UTF-8 -*-
"""Authon: Martysyuk Ilya
Title: Python Engineer
E-Mail: martysyuk@mail.ru
Phone: +7 (383) 299-1-373
Skype: martysyuk
"""

import sys
from pathlib import Path

class FileDecoder:

    def __init__(self, file_name):
        self.extension = Path(file_name).suffix[1:]
        method_name = str(self.extension) + '_file'
        try:
            method = getattr(self, method_name)
            return method(file_name)
        except AttributeError:
            print('Program can\'t recognize file format!')

    def doc_file(self, file_name):
        print('{} is a DOC file'.format(file_name))

    def xml_file(self, file_name):
        print('{} is a XML file'.format(file_name))

    def txt_file(self, file_name):
        print('{} is a TXT file'.format(file_name))


def main():
    try:
        argv = sys.argv[1]
        decoder = FileDecoder(argv)
    except IndexError:
        print('Вы должны указать имя файла!')

if __name__ == '__main__':
    main()