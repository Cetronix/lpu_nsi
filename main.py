#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re, tempfile
from grab import Grab
from urllib.request import urlretrieve

tmpdir = tempfile.mkdtemp()

try:
    print('Получение ссылки с сайта')
    g = Grab()
    g.go("https://www.orenfoms.ru/documents/index.php")
    # Собираем ссылку
    url = 'https://www.orenfoms.ru' + g.doc.select('//*[@id="content"]/div/section/div/section/div/div[2]/div[1]/div[1]/div/div/a').attr('href')
    # Получаем имя файла из URL
    print("URL: %s" % (url))
    result = re.match(r".*event3=(.*)&.*", url)
    if result.group(1).upper().find("NSI") == -1:
        print('Ссылка не содержит НСИ!')
        sys.exit(1)
    dst = tmpdir+'/'+result.group(1)
    urlretrieve(url, dst)
    print('Файл сохранен как %s' % (dst))
except:
    print('Ошибка загрузки сайта/файла')
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
cnx = mysql.connector.connect(user='demo',password='elcefabc', host='127.0.0.1', database='helper')
cursor = cnx.cursor()
update=False
with open(nsidir+'/update.sql','w') as f:
    print("DataBase\tXML File\tTable")
    for key in tables.tables:
        TabVerXml = tables.getversion(nsiroot, key)
        query = "SELECT version FROM tables WHERE name='"+key+"'"
        cursor.execute(query)
        for (version) in cursor:
            print("{}\t{}\t{}".format(version[0],TabVerXml,key), end='')
            if version[0] == TabVerXml:
                print("\t==")
            else:
                print("\t!=")
                update=True
                query = "TRUNCATE %s;\n%s\n" % (key,tables.getquery(nsiroot,key))
                query += "UPDATE tables SET version='%s' WHERE name='%s';" % (tables.getversion(nsiroot,key),key)
                f.write(query)
if update==True:
    print("Для обновления запусти: mysql -u demo -p helper < %s" % (nsidir+'/update.sql'))
cursor.close()
cnx.close()

