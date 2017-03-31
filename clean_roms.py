#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import shutil
import hashlib
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

host = config.get('MYSQL', 'host')
user = config.get('MYSQL', 'user')
passwd = config.get('MYSQL', 'passwd')
db = config.get('MYSQL', 'db')

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
cur = db.cursor()

source = config.get('PATH', 'romstoclean')
destination = config.get('PATH', 'romssource')

consoles = config.items('CONSOLES')

for key, console in consoles:

#    cur.execute("UPDATE "+console+" SET exist = NULL")

    cur.execute("SELECT * FROM "+console+" WHERE exist IS NULL")
    rows = cur.fetchall()

    directory = destination + console 
    if not os.path.exists(directory):
	os.makedirs(directory)

    for row in rows:
	name = row[2]
	md5 = row[7]

	files = source + console + '/' + name
	files_clean = destination + console + '/' + name

	if ( not os.path.isfile(files)):
	    print 'fichier non trouvé : ' + name
	else:
	    f = open(files, 'rb')
#	    f.seek(16) # skip the first 16 bytes for nes
	    rest = f.read()
	    m = hashlib.md5()
	    m.update(rest)
	    files_md5 = m.hexdigest().upper()

	    if md5 == files_md5:
		os.rename(files, files_clean)
		sql = "UPDATE "+console+" SET exist=%s WHERE name=%s"
		cur.execute( sql, ('OK', name))
    db.commit()

    print 'Premiere étape fini'

    for file in os.listdir(source + console + '/'):
	files = (os.path.join(source + console + '/' + file))

	f = open(files, 'rb')
#	f.seek(16) # skip the first 16 bytes for nes
	rest = f.read()
	m = hashlib.md5()
	m.update(rest)
	files_md5 = m.hexdigest().upper()

	cur.execute("SELECT * FROM "+console+" WHERE status IS NULL")
	rows = cur.fetchall()

	for row in rows:
	    if row[5] == files_md5 :
		files_name = row[2]
		print "Trouvé : " + file
		os.rename(files, source + console + '/' + files_name)

db.close()
