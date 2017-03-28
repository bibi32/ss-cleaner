#!/usr/bin/python
# -*- coding: utf-8 -*- 

import MySQLdb
import urllib2
import json
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

host = config.get('MYSQL', 'host')
user = config.get('MYSQL', 'user')
passwd = config.get('MYSQL', 'passwd')
db = config.get('MYSQL', 'db')

devid = 'xxx'
devpassword = 'yyy'
ssid = 'test'
sspassword = 'test'

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
cur = db.cursor()

consoles = config.items('CONSOLES')

for key, console in consoles:

    cur.execute("SELECT * FROM "+console+" WHERE nom_ss is NULL")
    rows = cur.fetchall()

    for row in rows:
	rom = row[2]
	romtaille = row[5]
	crc  = row[6]
	romnom = rom.replace(" ", "%20").replace("(", "%28").replace(")", "%29")

	url = "https://www.screenscraper.fr/api/jeuInfos.php?devid="+devid+"&devpassword="+devpassword+"&softname=zzz&output=json&ssid="+ssid+"&sspassword="+sspassword+"&crc="+crc+"&systemeid=1&romtype=rom&romnom="+romnom+"&romtaille="+romtaille
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req)

	try:
	    fichier_json = json.loads(f.read())

	    nom =  fichier_json["response"]["jeu"]["nom"]
	    system_ss = fichier_json["response"]["jeu"]["systemenom"]

	    nom_ss = (nom_ss.upper())

	    cur.execute("UPDATE "+console+" SET nom_ss=%s WHERE description=%s ", (nom_ss, rom))

	except ValueError, f:
	    print "ERROR"

    db.commit()
db.close()
