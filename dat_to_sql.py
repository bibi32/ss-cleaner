#!/usr/bin/python
# -*- coding: utf-8 -*- 

from lxml import etree
import sqlite3
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

nointro = config.get('PATH', 'datfilepath')

db = sqlite3.connect('nointro.db')
cur = db.cursor()

consoles = config.items('CONSOLES')

for key, console in consoles:

    datfile = nointro + config.get('DAT', console)

    cur.execute("DROP TABLE IF EXISTS "+console)
    cur.execute("CREATE TABLE IF NOT EXISTS %s (description varchar(200), name varchar(200), nom varchar(200), nom_ss varchar(200), size varchar(50), crc varchar(50), md5 varchar(50), sha1 varchar(50), exist varchar(5), status varchar(5))" % (console))

    print datfile

    tree = etree.parse(datfile)
    print tree
    for element in tree.iter('game'):
	description = element.find('description').text
	name = element.find("rom").attrib['name']
	size = element.find("rom").attrib['size']
	crc = element.find("rom").attrib['crc']
	md5 = element.find("rom").attrib['md5']
	sha1 = element.find("rom").attrib['sha1']

	print name

	sql = "INSERT INTO "+ console +" (description, name, size, crc, md5, sha1) VALUES (?, ?, ?, ?, ?, ?)"
	cur.execute( sql, (description, name, size, crc, md5, sha1))

	db.commit()

db.close()
