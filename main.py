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
# TODO: добавить удаление файла архива
print("Файлы распакованы в %s" % (nsidir))
# Поиск папки, содержащей папки REGIONAL и FEDERAL
from os import walk
for dirnames in walk(nsidir):
    position = dirnames[0].find("REGIONAL")
    if position!=-1:
        nsiroot = dirnames[0][0:position]
        print("Путь к папке REGIONAL %s" % (nsiroot))
        break
if len(nsidir)==0:
    print("Ошибка! Папка REGIONAL не найдена.")
    sys.exit(1)
print("Версии справочников:")
import tables, mysql.connector
cnx = mysql.connector.connect(user='',password='', host='127.0.0.1', database='')
cursor = cnx.cursor()
with open(nsidir+'/update.sql','w') as f:
    for key in tables.tables:
        query = "SELECT version FROM tables WHERE name='"+key+"'"
        cursor.execute(query)
        for (version) in cursor:
            print("DB: {}".format(version[0]))
        print("%s\t%s" % (tables.getversion(nsiroot,key),key))
        #print("Таблица %s -> %s" % (key, tables.tables[key]['path']))
        #print("Запрос для обновления:\n%s" % tables.getquery(nsiroot,key))
        query = "TRUNCARE %s;\n%s\n" % (key,tables.getquery(nsiroot,key))
        query += "UPDATE tables SET version='%s' WHERE name='%s';" % (tables.getversion(nsiroot,key),key)
        f.write(query)

print("Для обновления запусти: mysql -u demo -p helper < %s" % (nsidir+'/update.sql'))
cursor.close()
cnx.close()

