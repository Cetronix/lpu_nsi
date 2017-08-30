#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import feedparser, sys, re, tempfile
from grab import Grab
from urllib.request import urlretrieve

tmpdir = tempfile.mkdtemp()

try:
    # Загрузка RSS
    print("Загрузка RSS")
    rss = feedparser.parse('https://www.orenfoms.ru/documents/rss/')
    # print('%s -> %s' % (rss.entries[0].title,rss.entries[0].link))
    # Переход по ссылке
    print('Получение ссылки с сайта')
    g = Grab()
    g.go(rss.entries[0].link)
    # Собираем ссылку
    url = 'https://www.orenfoms.ru' + g.doc.select('//*[@id="content"]/div/section/div/section/div/div[2]/p[3]/a').attr(
        'href')
    # Получаем имя файла из URL
    result = re.match(r".*event3=(.*)&.*", url)
    dst = tmpdir+'/'+result.group(1)
    urlretrieve(url, dst)
    print('Файл сохранен как %s' % (dst))
except:
    print('Ошибка загрузки RSS/сайт/файл')
    sys.exit(1)
# Распаковка архива
import zipfile
nsidir = tmpdir +'/nsi'
zip_ref = zipfile.ZipFile(dst, 'r')
zip_ref.extractall(nsidir)
zip_ref.close()
print("Файлы распакованы в %s" % (nsidir))

'''
# Анализ файлов 
from xml.etree import ElementTree as ET
print("Версии справочников:")

xml_reg = {'depart': 'REGIONAL/DEPART.xml',
           'mkb': 'REGIONAL/MKB.xml',
           'ksg_g': 'REGIONAL/KSG_G.xml',
           'ksg_g_c': 'REGIONAL/KSG_G_C.xml'}
xml_fed = {'v002': 'FEDERAL/V002.xml'}
print("[ Региональные ]")
for key, value in xml_reg.items():
    root = ET.parse(nsidir+'/' + value).getroot()
    for zglv in root.iter('zglv'):
        print(key, "\t", zglv.find('date').text)
        break
print("[ Федеральные ]")
for key, value in xml_fed.items():
    root = ET.parse(nsidir+'/' + value).getroot()
    for zglv in root.iter('zglv'):
        print(key, "\t", zglv.get('date'))
        break
'''

import configparser
conf = configparser.RawConfigParser()



from tables import mkb
for key in mkb.name:
    print("%s -> %s" % (key, mkb.name[key]))
    mkb.getquery(nsidir+'/'+mkb.name[key])