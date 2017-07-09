# -*- coding: UTF-8 -*-
"""Authon: Martysyuk Ilya
Title: Python Engineer
E-Mail: martysyuk@mail.ru
Phone: +7 (383) 299-1-373
Skype: martysyuk
"""

s = "Test"

code_keys = ['qwertyuiopasdfghjklzxcvbnm1234567890!@#$%ˆ*()QWERTYUIOPASDFGHJKLZXCVBNM', '!@#$%ˆ*()0987654321MNBVCXZLKJHGFDSAQWERTYUIOPlkjhgfdsayuioptrewqzxcvmnb']

code = s.maketrans(code_keys[0], code_keys[1])
a = s.translate(code)
print(a)
code = a.maketrans(code_keys[1], code_keys[0])
a = a.translate(code)
print(a)
