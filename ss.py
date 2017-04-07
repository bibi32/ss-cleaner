#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sqlite3
import urllib
import urllib2
import json
import cgi
import base64
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

db = sqlite3.connect('nointro.db')
cur = db.cursor()

devid = config.get('ID', 'devid')
devid = base64.b64decode(devid)
devpassword = config.get('ID', 'devpassword')
devpassword = base64.b64decode(devpassword)

ssid = config.get('ID', 'ssid')
sspassword = config.get('ID', 'sspassword')

consoles = config.items('CONSOLES')

for key, console in consoles:

    systemeid = config.get('SYSTEMID', console)

    cur.execute("SELECT * FROM "+console+" WHERE nom_ss is NULL")
    rows = cur.fetchall()

    for row in rows:
	rom = row[1]
	romtaille = row[4]
	crc  = row[5]
	romnom = urllib.quote(rom, safe='')

	url = "https://www.screenscraper.fr/api/jeuInfos.php?devid="+devid+"&devpassword="+devpassword+"&softname=zzz&output=json&ssid="+ssid+"&sspassword="+sspassword+"&crc="+crc+"&systemeid="+systemeid+"&romtype=rom&romnom="+romnom+"&romtaille="+romtaille
#	url = "https://www.screenscraper.fr/api/jeuInfos.php?devid="+devid+"&devpassword="+devpassword+"&softname=zzz&output=json&crc="+crc
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req)

	try:
	    fichier_json = json.loads(f.read())

	    nom_ss =  fichier_json["response"]["jeu"]["nom"]
	    print nom_ss

	    cur.execute("UPDATE "+console+" SET nom_ss=? WHERE name=? ", (nom_ss, rom))

	except ValueError, f:
	    print "ERROR"

	db.commit()
db.close()
